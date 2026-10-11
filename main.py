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
        user_input=input("User:")

        answer=agent.run(user_input)

        print("Agent:", answer)


if __name__ == "__main__":
    main()