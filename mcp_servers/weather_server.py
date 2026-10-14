from mcp.server.mcpserver import MCPServer


server = MCPServer(
    name="weather-server"
)


@server.tool()
def get_weather(city: str) -> str:
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
        f"暂无{city}天气数据"
    )


if __name__ == "__main__":
    server.run()