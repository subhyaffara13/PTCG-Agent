
def _is_user_agent_tag(tag: Optional[str]) -> bool:
    """Determine whether a tag should be treated as a User-Agent tag."""
    if not tag:
        return False
    normalized_tag = tag.strip().lower()
    return normalized_tag.startswith("user-agent:") or normalized_tag.startswith(
        "user agent:"
    )

