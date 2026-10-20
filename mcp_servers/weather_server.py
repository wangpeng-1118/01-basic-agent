from mcp.server import MCPServer
import asyncio

server = MCPServer(
    name="weather-server",
    version="1.0.0",
    description="Weather query MCP Server"
)


@server.tool()
async def mcp_get_weather(city: str) -> str:
    """
    查询城市天气
    """

    weather_data = {
        "北京": "晴天，25°C",
        "上海": "多云，27°C",
        "武汉": "小雨，23°C",
    }

    return weather_data.get(
        city,
        f"暂无 {city} 的天气信息"
    )


async def main():

    await server.run_stdio_async()


if __name__ == "__main__":
    asyncio.run(main())