"""Tests for the ToolRegistry class."""
import pytest
from openai_toolchain.tools import ToolRegistry, tool

def test_register_tool(tool_registry):
    """Test registering a tool with the registry."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool
    def test_func(a: int, b: int = 1) -> int:
        """Add two numbers."""
        return a + b
    
    # Check that the tool was registered
    assert 'test_func' in tool_registry._tools
    tool_info = tool_registry._tools['test_func']
    assert tool_info['function'] is test_func
    assert tool_info['description'] == "Add two numbers."
    assert tool_info['parameters']['type'] == 'object'
    assert 'a' in tool_info['parameters']['properties']
    assert 'b' in tool_info['parameters']['properties']

def test_register_tool_with_name(tool_registry):
    """Test registering a tool with a custom name."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool(name="custom_name")
    def test_func():
        """Test function."""
        pass
    
    assert 'custom_name' in tool_registry._tools
    assert tool_registry._tools['custom_name']['function'] is test_func

def test_get_tool(tool_registry):
    """Test getting a registered tool."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool
    def test_func():
        """Test function."""
        return "success"
    
    tool_info = tool_registry.get_tool('test_func')
    assert tool_info['function'] is test_func
    assert tool_info['function']() == "success"

def test_get_nonexistent_tool(tool_registry):
    """Test getting a tool that doesn't exist."""
    # Clear any existing tools
    tool_registry._tools = {}
    assert tool_registry.get_tool('nonexistent') is None

def test_call_tool(tool_registry):
    """Test calling a registered tool."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
    
    result = tool_registry.call_tool('add', {'a': 2, 'b': 3})
    assert result == 5

def test_get_tool_schemas(tool_registry):
    """Test getting tool schemas in OpenAI format."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool
    def test_func(a: int):
        """Test function."""
        pass
    
    schemas = tool_registry.get_tool_schemas()
    assert len(schemas) == 1
    assert schemas[0]['type'] == 'function'
    assert schemas[0]['function']['name'] == 'test_func'
    assert 'parameters' in schemas[0]['function']
    assert schemas[0]['function']['parameters']['properties']['a']['type'] == 'number'

def test_clear_tools(tool_registry):
    """Test clearing all registered tools."""
    # Clear any existing tools
    tool_registry._tools = {}
    
    @tool
    def test_func():
        pass
    
    assert len(tool_registry._tools) == 1  # The just registered function
    tool_registry.clear()
    assert len(tool_registry._tools) == 0
