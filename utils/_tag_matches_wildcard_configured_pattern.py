
def _tag_matches_wildcard_configured_pattern(
    tags: Sequence[str], configured_tag: str
) -> bool:
    """
    Check if any of the request tags matches a wildcard configured pattern

    Args:
        tags: List[str] - The request tags
        configured_tag: str - The configured tag

    Returns:
        bool - True if any of the request tags matches the configured tag, False otherwise

    e.g.
    tags = ["User-Agent: curl/7.68.0", "User-Agent: python-requests/2.28.1", "prod"]
    configured_tag = "User-Agent: curl/*"
    _tag_matches_wildcard_configured_pattern(tags=tags, configured_tag=configured_tag) # True

    configured_tag = "User-Agent: python-requests/*"
    _tag_matches_wildcard_configured_pattern(tags=tags, configured_tag=configured_tag) # True

    configured_tag = "gm"
    _tag_matches_wildcard_configured_pattern(tags=tags, configured_tag=configured_tag) # False
    """
    import re

    from litellm.router_utils.pattern_match_deployments import PatternMatchRouter

    pattern_router = PatternMatchRouter()
    regex_pattern = pattern_router._pattern_to_regex(configured_tag)
    return any(re.match(pattern=regex_pattern, string=tag) for tag in tags)

