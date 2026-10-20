import asyncio

from agent.mcp_client import MCPClient



async def main():

    client = MCPClient(
        "mcp_servers/weather_server.py"
    )


    await client.connect()

    # 查看服务器提供的工具
    tools = await client.list_tools()


    for tool in tools:
        print(tool.name)
        print(tool.description)

    print("开始调用工具")

    # 实际调用天气工具
    result = await client.call_tool(
        "get_weather",
        {"city": "北京"}
    )

    print("工具调用结果:", repr(result))
    print("工具调用结束")


if __name__ == "__main__":
    asyncio.run(main())