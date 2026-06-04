from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def greet(name: str) -> str:
    """Generate a greeting."""
    return f"Hello, {name}!"


@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read a file from disk."""
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as err:
        return f"Error reading file: {err}"


@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


if __name__ == "__main__":
    mcp.run(transport="stdio")