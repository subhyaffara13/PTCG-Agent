
def _system_to_text(
    system: Optional[Union[str, List[Dict[str, Any]]]],
) -> str:
    """Flatten an Anthropic-style ``system`` value into a single string for
    token counting. Returns ``""`` when ``system`` carries no text."""
    if system is None:
        return ""
    if isinstance(system, str):
        return system
    parts: List[str] = []
    for block in system:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str) and text:
                parts.append(text)
    return "\n".join(parts)

