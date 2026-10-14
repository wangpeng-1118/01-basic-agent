import asyncio

from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

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

    