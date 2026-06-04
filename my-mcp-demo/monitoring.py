import logging
import time
from functools import wraps


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def monitor_tool(func):
    """
    Simple monitoring decorator.

    It logs:
    - tool name
    - execution time
    - success or error
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        start_time = time.time()

        logging.info(f"Tool started: {tool_name}")

        try:
            result = func(*args, **kwargs)

            duration = time.time() - start_time

            logging.info(
                f"Tool completed: {tool_name} | duration={duration:.4f}s | status=success"
            )

            return result

        except Exception as error:
            duration = time.time() - start_time

            logging.error(
                f"Tool failed: {tool_name} | duration={duration:.4f}s | "
                f"status=error | error={error}"
            )

            raise

    return wrapper


@monitor_tool
def add(a: int, b: int) -> int:
    return a + b


@monitor_tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@monitor_tool
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")

    return a / b


if __name__ == "__main__":
    print("Monitoring demo")

    print("add result:", add(2, 3))
    print("greet result:", greet("Olesya"))
    print("divide result:", divide(10, 2))

    # Uncomment this line if you want to test error logging:
    # print("divide error:", divide(10, 0))