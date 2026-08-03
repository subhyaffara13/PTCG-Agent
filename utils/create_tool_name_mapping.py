from typing import Any, Dict, List

def create_tool_name_mapping(
    tools: List[Dict[str, Any]],
) -> Dict[str, str]:
    """
    Create a mapping of truncated tool names to original names.

    Args:
        tools: List of tool definitions with 'name' field

    Returns:
        Dict mapping truncated names to original names (only for truncated tools)
    """
    mapping: Dict[str, str] = {}
    for tool in tools:
        original_name = tool.get("name", "")
        truncated_name = truncate_tool_name(original_name)
        if truncated_name != original_name:
            mapping[truncated_name] = original_name
    return mapping

