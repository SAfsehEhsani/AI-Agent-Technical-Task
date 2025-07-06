# part1/tools/__init__.py
# Expose the tool classes/instances so they can be imported from part1.tools
from .base import BaseTool # Export BaseTool if you want it accessible
from .tool_one import PlaceholderToolOne # Import the class
from .tool_two import PlaceholderToolTwo # Import the class

# Instantiate your tools here
# Remember to replace these with your actual tool implementations
AVAILABLE_TOOLS = [
    PlaceholderToolOne(),
    PlaceholderToolTwo(),
    # Add instances of your real tool classes here
]

# Create a dictionary for easy lookup by name
TOOL_MAP = {tool.name: tool for tool in AVAILABLE_TOOLS}

# Export the list and map
__all__ = ["BaseTool", "AVAILABLE_TOOLS", "TOOL_MAP", "PlaceholderToolOne", "PlaceholderToolTwo"]