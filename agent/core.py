import json
from .session_manager import SessionManager

class Agent:

    def __init__(
        self,
        client,
        tools,
        tool_schemas,
        model="deepseek-flash"
    ):
        self.client = client
        self.tools = tools
        self.tool_schemas = tool_schemas
        self.model = model

        # Session管理器
        self.session_manager = SessionManager()

    
    def run(self, user_input, session_id="default"):
        
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
        
        # 调用LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=session.get_messages(),
            tools=self.tool_schemas
        )

        # response中的message，里面包含LLM返回的tool工具调用相关的信息
        message = response.choices[0].message

        if message.tool_calls:

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

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                tool_function = (
                    self.tools[tool_name]
                )

                result = tool_function(**arguments)
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
            

            final_response = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=self.session.get_messages()
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



