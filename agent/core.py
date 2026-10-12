import json

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

        # 保存上下文
        self.messages = []
    
    def run(self, user_input):
        # 原始输入给LLM的message
        self.messages.append(
            {
                "role":"user",
                "content":user_input
            }
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tool_schemas
        )

        # response中的message，里面包含LLM返回的tool工具调用相关的信息
        message = response.choices[0].message

        #遍历所有的tool调用
        if message.tool_calls:

            tool_messages = []

            for tool_call in message.tool_calls:

                tool_name = (
                    tool_call.function.name
                )

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

            assistant_message = message.model_dump()

            if assistant_message["content"] is None:
                assistant_message["content"] = ""
            
            self.messages.extend(
                [
                    assistant_message,
                    *tool_messages
                ]
            )

            # self.messages.extend(
            #     [
            #         message,
            #         *tool_messages
            #     ]
            # )

            # #测试
            # print(json.dumps(
            #     messages,
            #     indent=4,
            #     ensure_ascii=False,
            #     default=str
            # ))

            final_response = (
                self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
            )

            return (final_response.choices[0].message.content)
        else:
            return message.content




