"""Tool registration and management for OpenAI function calling."""

import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union, get_type_hints


class ToolError(Exception):
    """Exception raised for errors in tool registration or execution."""
    pass


class ToolRegistry:
    """Registry for AI tools with automatic schema generation."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def register(
        self,
        func: Optional[Callable] = None,
        *,
        name: Optional[str] = None,
        **kwargs
    ) -> Callable:
        """Register a function as a tool.

        Can be used as a decorator with or without arguments.

        Args:
            func: The function to register (automatically passed when used as decorator)
            name: Optional custom name for the tool
            **kwargs: Additional tool metadata

        Returns:
            The decorated function or a decorator
        """
        def decorator(f: Callable) -> Callable:
            nonlocal name

            tool_name = name or f.__name__
            tool_description = (f.__doc__ or "").strip()

            # Store the tool
            self._tools[tool_name] = {
                'function': f,
                'description': tool_description,
                'parameters': self._get_parameters_schema(f),
                'metadata': kwargs
            }

            return f

        if func is not None:
            return decorator(func)
        return decorator

    def _get_parameters_schema(self, func: Callable) -> Dict[str, Any]:
        """Generate OpenAPI schema for function parameters."""
        sig = inspect.signature(func)
        parameters = {}
        required = []
        type_hints = get_type_hints(func)

        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue

            param_type = type_hints.get(param_name, str)
            param_info = self._get_parameter_info(param, param_type)
            parameters[param_name] = param_info

            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        schema = {
            'type': 'object',
            'properties': parameters
        }

        if required:
            schema['required'] = required

        return schema

    def _get_parameter_info(self, param: inspect.Parameter, param_type: Type) -> Dict[str, Any]:
        """Get parameter information for the schema."""
        param_info = {'type': self._get_type_name(param_type)}

        # Add description if available
        if param.annotation != inspect.Parameter.empty:
            param_info['description'] = str(param.annotation)

        # Add default value if available
        if param.default != inspect.Parameter.empty:
            param_info['default'] = param.default

        return param_info

    def _get_type_name(self, type_: Type) -> str:
        """Convert Python type to JSON schema type name."""
        if type_ == str:
            return 'string'
        elif type_ in (int, float):
            return 'number'
        elif type_ == bool:
            return 'boolean'
        return 'string'

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a registered tool by name."""
        return self._tools.get(name)

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered tool by name with the given arguments."""
        tool = self.get_tool(name)
        if not tool:
            raise ToolError(f"Tool '{name}' not found")

        try:
            return tool['function'](**arguments)
        except Exception as e:
            raise ToolError(f"Error calling tool '{name}': {e}") from e

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get all registered tools in OpenAI format."""
        return [
            {
                'type': 'function',
                'function': {
                    'name': name,
                    'description': tool['description'],
                    'parameters': tool['parameters']
                }
            }
            for name, tool in self._tools.items()
        ]

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()


# Global registry instance
tool_registry = ToolRegistry()

# Decorator for registering tools
def tool(
    func_or_name: Optional[Union[Callable, str]] = None,
    **kwargs
) -> Callable:
    """Decorator to register a function as a tool.

    Can be used as:
    - @tool
    - @tool(name="custom_name")
    - @tool("custom_name")
    """
    if isinstance(func_or_name, str):
        # @tool("name")
        name = func_or_name
        return lambda f: tool_registry.register(f, name=name, **kwargs)
    elif callable(func_or_name):
        # @tool
        return tool_registry.register(func_or_name, **kwargs)
    else:
        # @tool(name="name")
        return lambda f: tool_registry.register(f, **kwargs)
