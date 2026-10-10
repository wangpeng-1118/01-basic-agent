from openai import OpenAI
import os
import json

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def get_weather(city):
    """查询天气"""
    weather_data = {
        "北京": "晴，25°C",
        "上海": "多云，27°C",
        "武汉": "小雨，23°C",
    }

    return weather_data.get(city, f"暂时没有{city}的天气数据")


def main():
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "user",
                "content": "北京今天天气怎么样？",
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

        # 真正执行python 函数
        if tool_name == "get_weather":
            result = get_weather(
                arguments["city"]
            )

            print("工具执行结果：", result)

            # 将工具执行的结果传给LLM，得到LLM最终的输出
            messages = [
                {
                    "role": "user",
                    "content": "北京今天天气怎么样？",
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