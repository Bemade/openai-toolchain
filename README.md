# OpenAI Toolchain

A Python library for working with OpenAI's function calling API.

## Installation

```bash
pip install openai-toolchain
```

## Quick Start

```python
from openai_toolchain import tool, OpenAIClient

# Register a function as a tool
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 22 {unit}"

# Register a function with a custom name
@tool("get_forecast")
def get_forecast_function(location: str, days: int = 1) -> str:
    """Get a weather forecast for a location.
    
    Args:
        location: The city to get the forecast for
        days: Number of days to forecast (1-5)
    """
    return f"{days}-day forecast for {location}: Sunny"

# Initialize the client with your API key
client = OpenAIClient(api_key="your-api-key")

# Chat with automatic tool calling
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the weather in Toronto?"}],
    tools=["get_weather"]  # Optional: specify which tools to use
)

print(response)
```

## Features

### 1. Tool Registration

Use the `@tool` decorator to register functions as tools:

```python
from openai_toolchain import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"
```

### 2. Chat with Automatic Tool Calling

The `chat_with_tools` method handles tool calls automatically:

```python
client = OpenAIClient(api_key="your-api-key")

response = client.chat_with_tools(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Search for the latest Python news"}
    ],
    tools=["search_web"],
    model="gpt-4"  # Optional: specify a different model
)
```

### 3. Accessing Registered Tools

You can access registered tools directly:

```python
from openai_toolchain import tool_registry

# Get all registered tools
tools = tool_registry.get_tool_schemas()

# Call a tool directly
result = tool_registry.call_tool("get_weather", {"location": "Paris", "unit": "fahrenheit"})
```

## API Reference

### `@tool` decorator

Register a function as a tool:

```python
from openai_toolchain import tool

@tool
def my_function(param: str) -> str:
    """Function documentation."""
    return f"Result for {param}"
```

### `tool_registry`

The global registry instance with these methods:

- `register(func, **kwargs)`: Register a function as a tool
- `get_tool(name)`: Get a registered tool by name
- `call_tool(name, arguments)`: Call a registered tool by name with arguments
- `get_openai_tools()`: Get all tools in OpenAI format

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
