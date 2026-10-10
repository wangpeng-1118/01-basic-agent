from openai import OpenAI
import os
import json
from tools import TOOLS

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def main():
    user_input = input("User: ")
    content = user_input

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "查询指定城市的天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "要查询天气的城市",
                            }
                        },
                        "required": ["city"],
                    },
                },
            },

            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "计算数学表达式",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string"
                            }
                        },
                        "required": ["expression"]
                    }
                }
            }
        ],
    )

    message = response.choices[0].message

    #查看模型是否要求调用工具
    if message.tool_calls:
        tool_call = message.tool_calls[0]

        # 获取工具名称
        tool_name = tool_call.function.name

        # 获取工具参数
        arguments = json.loads(
            tool_call.function.arguments
        )

        print("模型的选择工具：", tool_name)
        print("模型提供的参数：", arguments)

        
        tool_function = TOOLS[tool_name]
        result = tool_function(**arguments)

        # 将工具执行的结果传给LLM，得到LLM最终的输出
        messages = [
            {
                "role": "user",
                "content": content,
            },
            message,
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            },
        ]

        final_response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
        )

        print(
            "final_answer:", final_response.choices[0].message.content
        )


if __name__ == "__main__":
    main()