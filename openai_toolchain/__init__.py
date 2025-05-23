"""OpenAI Toolchain - A Python library for working with OpenAI's function calling API."""

# Version is managed by setuptools_scm
from typing import TYPE_CHECKING

from .client import OpenAIClient
from .tools import ToolError, tool, tool_registry

if TYPE_CHECKING or not hasattr("_version", "version"):
    # For mypy or when _version is not available
    __version__ = "0.0.0"
else:
    from ._version import version as __version__  # type: ignore[import-not-found]

__all__ = ["ToolError", "tool", "OpenAIClient", "tool_registry"]
