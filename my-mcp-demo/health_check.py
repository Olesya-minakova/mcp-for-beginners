import time


def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "my-mcp-demo"
    }


if __name__ == "__main__":
    print(health_check())