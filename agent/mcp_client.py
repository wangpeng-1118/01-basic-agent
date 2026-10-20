import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

"""
async 用来声明"这个函数可以被异步调度"
await 用来声明"这里需要等待一个异步结果，在等待期间可以让出执行权"
"""

class MCPClient:
    def __init__(self, server_path):

        self.server_path = server_path
        self.session = None

    async def connect(self):

        server_params = StdioServerParameters(
            command="python",
            args=[
                self.server_path
            ]
        )

        self.stdio_transport = (
            stdio_client(server_params)
        )

        self.read, self.write = await(
            self.stdio_transport.__aenter__()
        )

        self.session = ClientSession(
            self.read,
            self.write
        )

        await self.session.__aenter__()

        await self.session.initialize()

    async def list_tools(self):

        response = await(
            self.session.list_tools()
        )

        return response.tools

    
    # 传参为工具的名称以及传给工具的参数
    async def call_tool(self, tool_name, arguments):
        """调用 MCP Server 提供的工具"""

        response = await self.session.call_tool(
            tool_name,
            arguments
        )

        # print("MCP 原始响应：", repr(response))
        # print("MCP 响应内容:", repr(response.content))

        # 提取工具返回的文本
        results = []

        for item in response.content:
            # hasattr：python中的内置函数，用于判断一个对象中是否具有指定的属性或方法
            if hasattr(item, "text"):
                results.append(item.text)

        return "\n".join(results)

    