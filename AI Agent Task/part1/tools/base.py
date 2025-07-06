# part1/tools/base.py
from abc import ABC, abstractmethod
from typing import Any

class BaseTool(ABC):
    """Abstract base class for agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the tool."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """A description of the tool's function, used by the agent."""
        pass

    # Decide if run should be async if your tools do async operations (like API calls)
    @abstractmethod
    # async def run(self, tool_input: Any) -> Any: # Example for async
    def run(self, tool_input: Any) -> Any: # Example for sync
        """Execute the tool with the given input."""
        pass