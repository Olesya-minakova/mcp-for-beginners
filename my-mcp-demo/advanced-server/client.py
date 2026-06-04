import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            print("Available tools:")
            for tool in tools.tools:
                print("-", tool.name)

            add_result = await session.call_tool(
                "add",
                arguments={"a": 2, "b": 3},
            )
            print("\nadd result:")
            print(add_result.content)

            multiply_result = await session.call_tool(
                "multiply",
                arguments={"a": 4, "b": 5},
            )
            print("\nmultiply result:")
            print(multiply_result.content)

            greet_result = await session.call_tool(
                "greet",
                arguments={"name": "Olesya"},
            )
            print("\ngreet result:")
            print(greet_result.content)


if __name__ == "__main__":
    asyncio.run(run())