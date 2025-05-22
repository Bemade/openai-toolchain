"""Example of using the OpenAI Toolchain with environment variables for configuration.

Set these environment variables:
- OPENAI_API_KEY: Your OpenAI API key
- OPENAI_BASE_URL: (Optional) Base URL for the API (defaults to OpenAI's API)
"""

import os
import json
from typing import Literal
from openai import OpenAI
from openai_toolchain import tool, tool_registry, ToolError

# Register tools using the decorator
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 22 {unit}"

@tool
def get_forecast(location: str, days: int = 1) -> str:
    """Get a weather forecast for a location."""
    return f"{days}-day forecast for {location}: Sunny"

def main():
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set\n"
                      "Please set your OpenAI API key and try again")
        return

    # Initialize the OpenAI client
    base_url = os.getenv("OPENAI_BASE_URL")
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    # Get tools in OpenAI format
    tools = tool_registry.get_openai_tools()

    print("Available tools:")
    for tool_spec in tools:
        print(f"- {tool_spec['function']['name']}: {tool_spec['function']['description']}")

    print("\nExample conversation:")
    print("User: What's the weather in Toronto and what's the forecast?")

    # Example of using the tools with the OpenAI client
    response = client.chat.completions.create(
        model="POP.qwen3:30b",
        messages=[{"role": "user", "content": "What's the weather in Toronto and what's the forecast for tomorrow?"}],
        tools=tools,
        tool_choice="auto"
    )

    # Process tool calls
    message = response.choices[0].message
    if message.tool_calls:
        print("\nTool calls detected:")
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            print(f"\nCalling {func_name} with args: {args}")

            try:
                # Call the tool
                result = tool_registry.call_tool(func_name, args)
                _logger.info(f"Result: {result}")

                # In a real app, you would send the result back to the model

            except ToolError as e:
                _logger.error(f"Error: {e}")
    else:
        print("\nNo tool calls in response:")
        print(message.content)

if __name__ == "__main__":
    main()
