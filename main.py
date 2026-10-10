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

    # 将模型返回对象转换为 Python 字典
    response_dict = response.model_dump(mode="json")

    # 保存为格式化的 JSON 文件
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(
            response_dict,
            f,
            ensure_ascii=False,
            indent=4,
        )

    print("模型返回结果已保存到 response.json")


if __name__ == "__main__":
    main()