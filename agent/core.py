import json
from .session_manager import SessionManager
import asyncio

class Agent:

    def __init__(
        self,
        client,
        tools,
        tool_schemas,
        model="deepseek-flash",
        mcp_client=None,
        mcp_tools=None
    ):
        self.client = client
        self.tools = tools
        self.tool_schemas = tool_schemas
        self.model = model

        # Session管理器
        self.session_manager = SessionManager()

        # MCP 客户端
        self.mcp_client = mcp_client

        # MCP 服务器提供的工具
        self.mcp_tools = mcp_tools or []

    
    async def run(self, user_input, session_id="default"):
        print("[test1] 进入 Agent.run")
        session = self.session_manager.get_session(
            session_id
        )

        user_message = {
            "role": "user",
            "content": user_input
        }
        session.add_message(
            user_message
        )

        # print("[test2] 准备请求 Deepseek")
        # # 调用LLM
        # response = self.client.chat.completions.create(
        #     model=self.model,
        #     messages=session.get_messages(),
        #     tools=self.get_all_tool_schemas()
        # )

        # print("[test3] 已收到Deepseek响应")

        print("[调试2] 准备请求 DeepSeek")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=session.get_messages(),
                tools=self.get_all_tool_schemas(),
                timeout=30
            )

            print("[调试3] 已收到 DeepSeek 响应")

        except Exception as e:
            print("[错误] DeepSeek 请求失败:", repr(e))
            raise


        # response中的message，里面包含LLM返回的tool工具调用相关的信息
        message = response.choices[0].message

        
        if message.tool_calls:
            print("[test4] 开始处理工具调用")
            tool_messages = []

            assistant_message = {
                "role": "assistant",
                "content":"",
                "tool_calls":[]
            }
            # 遍历所有工具的调用
            for tool_call in message.tool_calls:

                assistant_message["tool_calls"].append(
                    {
                        "id":tool_call.id,
                        "type":"function",
                        "function":{
                            "name":
                            tool_call.function.name,
                            "arguments":
                            tool_call.function.arguments
                        }
                    }
                )

                # tool_name = tool_call.function.name

                # arguments = json.loads(
                #     tool_call.function.arguments
                # )

                # tool_function = (
                #     self.tools[tool_name]
                # )

                # if tool_name in self.tools:
                #     # 本地python工具
                #     result = tool_function(**arguments)
                # else:
                #     # MCP工具
                #     print("[test5] 准备调用MCP工具", tool_name)
                #     result = await self.mcp_client.call_tool(
                #         tool_name,
                #         arguments
                #     )
                #     print("[test6] MCP 工具返回：",repr(result))

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print(f"[调试] 工具名称：{tool_name}", flush=True)
                print(f"[调试] 工具参数：{arguments}", flush=True)

                if tool_name in self.tools:
                    # 本地 Python 工具
                    print("[test5] 准备调用本地工具", flush=True)

                    tool_function = self.tools[tool_name]
                    result = tool_function(**arguments)

                    print("[test6] 本地工具返回：", repr(result), flush=True)
                else:
                    # MCP工具
                    print("[test5] 准备调用 MCP 工具", tool_name, flush=True)

                    result = await self.mcp_client.call_tool(
                        tool_name,
                        arguments
                    )

                    print("[test6] MCP 工具返回：", repr(result), flush=True)

                # 通过tool工具之后得到对应的message
                tool_messages.append(
                        {
                            "role":"tool",
                            "tool_call_id":tool_call.id,
                            "content":result
                        }
                )
            
            # 保存assistant message
            session.add_message(
                assistant_message
            )
            
            # 保存工具结果
            for tool_message in tool_messages:

                session.add_message(
                    tool_message
                )
            
            print("[test7] 准备请求模型生成最终回答")
            final_response = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=session.get_messages()
                )
            )

            final_message = (final_response.choices[0].message.content)

            # 保存最终回答
            session.add_message(
                {
                    "role":"assistant",
                    "content":final_message
                }
            )

            return final_message
        else:
            
            answer = message.content

            session.add_message(
                {
                    "role":"assistant",
                    "content":answer
                }
            )

            return answer

    def get_all_tool_schemas(self):
        schemas = list(self.tool_schemas)

        for tool in self.mcp_tools:
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema
                }
            })

        return schemas


