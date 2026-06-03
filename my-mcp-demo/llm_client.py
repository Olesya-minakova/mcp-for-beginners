from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import asyncio
import json
import os

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential


server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
)


def convert_to_llm_tool(tool):
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema.get("properties", {}),
                "required": tool.inputSchema.get("required", []),
            },
        },
    }


def call_llm(prompt, functions):
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use tools when needed.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model_name,
        tools=functions,
        temperature=0,
        max_tokens=1000,
    )

    response_message = response.choices[0].message

    functions_to_call = []

    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            functions_to_call.append({"name": name, "args": args})

    return functions_to_call


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            functions = []
            print("Available MCP tools:")
            for tool in tools.tools:
                print("-", tool.name)
                functions.append(convert_to_llm_tool(tool))

            prompt = "Add 2 and 20"

            print("\nUser prompt:")
            print(prompt)

            functions_to_call = call_llm(prompt, functions)

            print("\nLLM selected tools:")
            print(functions_to_call)

            for function_call in functions_to_call:
                result = await session.call_tool(
                    function_call["name"],
                    arguments=function_call["args"],
                )

                print("\nTool result:")
                print(result.content)


if __name__ == "__main__":
    asyncio.run(run())