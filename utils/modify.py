from typing import Any, Dict, List, Optional

def modify(
    texts: Optional[List[str]] = None,
    images: Optional[List[Any]] = None,
    tool_calls: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """
    Modify the request/response content.

    Args:
        texts: Modified text content (if None, keeps original)
        images: Modified image content (if None, keeps original)
        tool_calls: Modified tool calls (if None, keeps original)

    Returns:
        Dict indicating the content should be modified
    """
    result: Dict[str, Any] = {"action": "modify"}
    if texts is not None:
        result["texts"] = texts
    if images is not None:
        result["images"] = images
    if tool_calls is not None:
        result["tool_calls"] = tool_calls
    return result

