import asyncio

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

from tools import tools


server = Server("advanced-demo-server")


def pydantic_to_json(model):
    return model.model_json_schema()


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    tool_list = []

    for tool in tools.values():
        tool_list.append(
            types.Tool(
                name=tool["name"],
                description=tool["description"],
                inputSchema=pydantic_to_json(tool["input_schema"]),
            )
        )

    return tool_list


@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict | None,
) -> list[types.TextContent]:
    if name not in tools:
        raise ValueError(f"Unknown tool: {name}")

    tool = tools[name]

    try:
        result = await tool["handler"](arguments or {})
    except Exception as e:
        raise ValueError(f"Error calling tool {name}: {str(e)}")

    return [
        types.TextContent(
            type="text",
            text=str(result),
        )
    ]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())