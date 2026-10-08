from openai import OpenAI
import os


client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "user",
            "content": "你好，请介绍一下你自己。",
        }
    ],
)

print(response.choices[0].message.content)
