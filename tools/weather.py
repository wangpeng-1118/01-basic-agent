

def get_weather(city) -> str:
    """
    查询指定城市的天气

    Args:
        city:
            城市名称

    Returns:
        天气信息
    """

    data = {
        "北京": "晴天，25°C",
        "上海": "多云，27°C",
        "武汉": "小雨，23°C",
        "深圳": "阴天，28°C",
    }

    return data.get(
        city,
        "暂无天气信息"
    )
