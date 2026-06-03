from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio


server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("Connected to MCP server")

            # List available tools
            tools = await session.list_tools()
            print("\nTOOLS:")
            for tool in tools.tools:
                print("-", tool.name)

            # Call the add tool
            result = await session.call_tool(
                "add",
                arguments={
                    "a": 2,
                    "b": 3
                }
            )

            print("\nRESULT OF add(2, 3):")
            print(result.content)


if __name__ == "__main__":
    asyncio.run(run())