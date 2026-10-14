import asyncio

from agent.mcp_client import MCPClient



async def main():

    client = MCPClient(
        "mcp_servers/weather_server.py"
    )


    await client.connect()


    tools = await client.list_tools()


    for tool in tools:
        print(tool.name)
        print(tool.description)



if __name__ == "__main__":
    asyncio.run(main())