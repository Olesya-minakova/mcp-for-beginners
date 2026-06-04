from .schema import GreetInputModel


async def greet_handler(args) -> str:
    try:
        input_model = GreetInputModel(**args)
    except Exception as e:
        raise ValueError(f"Invalid input: {str(e)}")

    return f"Hello, {input_model.name}!"


tool_greet = {
    "name": "greet",
    "description": "Generates a greeting",
    "input_schema": GreetInputModel,
    "handler": greet_handler,
}