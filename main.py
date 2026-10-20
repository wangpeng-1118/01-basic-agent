import asyncio
import os
import json

from openai import OpenAI
from tools import TOOLS, TOOL_SCHEMAS
from agent.core import Agent
from agent.mcp_client import MCPClient

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


async def main():
    # 1.创建MCP Client
    mcp_client = MCPClient(
        "mcp_servers/weather_server.py"
    )

    # 2.链接MCP Server
    await mcp_client.connect()

    # 3.获取 MCP 工具列表
    mcp_tools  = await mcp_client.list_tools()

    print("已连接 MCP Server")
    print("MCP 工具列表：")

    for tool in mcp_tools:
        print(f"- {tool.name}: {tool.description}")


    # 4.创建Agent，并传入MCP相关信息
    print("准备创建 Agent")
    agent = Agent(
        client=client,
        tools=TOOLS,
        tool_schemas=TOOL_SCHEMAS,
        mcp_client=mcp_client,
        mcp_tools=mcp_tools,
    )

    print("Agent 创建成功")
    print("准备进入输入循环")

    # 5.循环接收用户输入
    while True:

        user_id = input("User ID:")
        if user_id.lower() == "exit":
            print("quit command: User ID")
            break

        user_input=input("Message:")
        if user_input.lower() == "exit":
            print("qiut command: Message")
            break

        answer= await agent.run(user_input, session_id=user_id)

        print("Agent:", answer)

    print("while loop ended")
    print("main coroutine is about to return")


if __name__ == "__main__":
    print("ready for main")
    asyncio.run(main())
    print("function main is over")
