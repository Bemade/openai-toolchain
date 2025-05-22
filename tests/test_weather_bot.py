"""Integration tests for the weather bot example with real API calls."""

import os
import sys
import json
import logging
import pytest
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now we can import from the package directly
from openai_toolchain import tool, OpenAIClient, tool_registry

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Skip if we don't have the required environment variables
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set"
)

# Define our test tools
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 22 {unit}"

@tool
def get_forecast(location: str, days: int = 1) -> str:
    """Get a weather forecast for a location."""
    return f"{days}-day forecast for {location}: Sunny"

def print_message(role: str, content: str, tool_calls=None):
    """Print a formatted message with role and content."""
    print(f"\n{'='*80}")
    print(f"{role.upper()}:")
    if tool_calls:
        print("  Tool calls:")
        for call in tool_calls:
            print(f"  - {call.function.name}: {call.function.arguments}")
    if content:
        print(f"  {content}")
    print("="*80)

def test_weather_bot_integration(tool_registry):
    """Test the weather bot with the real API using OpenAIClient."""
    # Clear any existing tools
    tool_registry._tools = {}

    # Define our test tools
    @tool
    def get_weather(location: str, unit: str = "celsius") -> str:
        """Get the current weather in a given location."""
        return f"The weather in {location} is 22 {unit}"

    @tool
    def get_forecast(location: str, days: int = 1) -> str:
        """Get a weather forecast for a location."""
        return f"{days}-day forecast for {location}: Sunny"

    # Initialize the client with our tools
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    print("\n" + "#"*80)
    print("Initializing OpenAIClient...")
    print(f"Model: POP.qwen3:30b")
    print(f"Base URL: {base_url}")
    print("#"*80 + "\n")

    client = OpenAIClient(
        api_key=api_key,
        base_url=base_url,
        default_model="POP.qwen3:30b"
    )

    # Debug: Print registered tools and their structure
    print("\n" + "#"*40 + " REGISTERED TOOLS " + "#"*40)
    print(f"\nTool registry contents: {tool_registry._tools}")
    for name, tool_info in tool_registry._tools.items():
        print(f"\nTool: {name}")
        print(f"Type: {type(tool_info)}")
        if isinstance(tool_info, dict):
            print("Keys:", tool_info.keys())
            if 'function' in tool_info:
                print(f"Function: {tool_info['function'].__name__ if callable(tool_info['function']) else tool_info['function']}")
            if 'schema' in tool_info:
                print(f"Schema: {tool_info['schema']}")
        print("Full tool info:", tool_info)
    print("#"*80 + "\n")

    # Test 1: Simple weather query
    print("\n" + "="*40 + " TEST 1: SIMPLE WEATHER QUERY " + "="*40)
    user_message = "What's the weather like in Toronto?"
    print_message("User", user_message)

    response = client.chat_with_tools(
        messages=[{"role": "user", "content": user_message}],
        max_tool_calls=5
    )

    print_message("Assistant", response)

    # Verify the response includes the expected weather information
    assert response is not None
    assert "22" in response  # Should include the temperature from our mock
    assert "Toronto" in response

    # Test 2: Complex query using multiple tools
    print("\n" + "="*40 + " TEST 2: COMPLEX QUERY " + "="*40)
    user_message = "What's the weather like in Toronto and what's the forecast for tomorrow?"
    print_message("User", user_message)

    response = client.chat_with_tools(
        messages=[{"role": "user", "content": user_message}],
        max_tool_calls=5
    )

    print_message("Assistant", response)

    # Verify we got a response that includes both current weather and forecast
    assert response is not None
    assert "22" in response  # Current temp
    assert "forecast" in response.lower()
