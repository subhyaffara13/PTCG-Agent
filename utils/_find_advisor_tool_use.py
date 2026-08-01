
def _find_advisor_tool_use(response: Any) -> Optional[Dict]:
    """Return the first tool_use block with name='advisor', or None."""
    content = response.get("content") if isinstance(response, dict) else []
    if not isinstance(content, list):
        return None
    for block in content:
        if (
            isinstance(block, dict)
            and block.get("type") == "tool_use"
            and block.get("name") == "advisor"
        ):
            return block
    return None

