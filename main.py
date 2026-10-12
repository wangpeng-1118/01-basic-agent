from openai import OpenAI
import os
import json
from tools import TOOLS, TOOL_SCHEMAS
from agent.core import Agent

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


def main():
    agent = Agent(
        client=client,
        tools=TOOLS,
        tool_schemas=TOOL_SCHEMAS
    )

    while True:

        user_id = input("User ID:")

        user_input=input("Message:")

        answer=agent.run(user_input, session_id=user_id)

        print("Agent:", answer)


if __name__ == "__main__":
    main()