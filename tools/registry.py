from .weather import get_weather
from .calculator import calculate

TOOLS = {
    "get_weather": get_weather,
    "calculate": calculate,
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description":"查询指定城市的天气",
            "parameters":{
                "type": "object",
                "properties":{
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required":[
                    "city"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description":"计算数学表达式",
            "parameters":{
                "type": "object",
                "properties":{
                    "expression": {
                        "type": "string",
                        "description": "数学表达式"
                    }
                },
                "required":[
                    "expression"
                ]
            }
        }
    },
]