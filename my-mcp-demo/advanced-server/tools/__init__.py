from .add import tool_add
from .multiply import tool_multiply
from .greet import tool_greet


tools = {
    tool_add["name"]: tool_add,
    tool_multiply["name"]: tool_multiply,
    tool_greet["name"]: tool_greet,
}