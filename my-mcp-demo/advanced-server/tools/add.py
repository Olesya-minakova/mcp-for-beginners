from .schema import AddInputModel


async def add_handler(args) -> float:
    try:
        input_model = AddInputModel(**args)
    except Exception as e:
        raise ValueError(f"Invalid input: {str(e)}")

    return input_model.a + input_model.b


tool_add = {
    "name": "add",
    "description": "Adds two numbers",
    "input_schema": AddInputModel,
    "handler": add_handler,
}