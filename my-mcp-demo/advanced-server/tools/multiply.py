from .schema import MultiplyInputModel


async def multiply_handler(args) -> float:
    try:
        input_model = MultiplyInputModel(**args)
    except Exception as e:
        raise ValueError(f"Invalid input: {str(e)}")

    return input_model.a * input_model.b


tool_multiply = {
    "name": "multiply",
    "description": "Multiplies two numbers",
    "input_schema": MultiplyInputModel,
    "handler": multiply_handler,
}