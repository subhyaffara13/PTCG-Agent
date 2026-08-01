
def get_custom_labels_from_tags(tags: Sequence[str]) -> Dict[str, str]:
    """
    Get custom labels from tags based on admin configuration.

    Supports both exact matches and wildcard patterns:
    - Exact match: "prod" matches "prod" exactly
    - Wildcard pattern: "User-Agent: curl/*" matches "User-Agent: curl/7.68.0"

    Reuses PatternMatchRouter for wildcard pattern matching.

    Returns dict of label_name: "true" if the tag matches the configured tag, "false" otherwise

    {
        "tag_User-Agent_curl": "true",
        "tag_User-Agent_python_requests": "false",
        "tag_Environment_prod": "true",
        "tag_Environment_dev": "false",
        "tag_Service_api_gateway_v2": "true",
        "tag_Service_web_app_v1": "false",
    }
    """

    from litellm.types.integrations.prometheus import _sanitize_prometheus_label_name

    configured_tags = litellm.custom_prometheus_tags
    if configured_tags is None or len(configured_tags) == 0:
        return {}

    result: Dict[str, str] = {}

    for configured_tag in configured_tags:
        label_name = _sanitize_prometheus_label_name(f"tag_{configured_tag}")

        # Check for exact match first (backwards compatibility)
        if configured_tag in tags:
            result[label_name] = "true"
            continue

        # Use PatternMatchRouter for wildcard pattern matching
        if "*" in configured_tag and _tag_matches_wildcard_configured_pattern(
            tags=tags, configured_tag=configured_tag
        ):
            result[label_name] = "true"
            continue

        # No match found
        result[label_name] = "false"

    return result

