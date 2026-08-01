
def _filter_keys_by_tags(keys: list, tag_patterns: list) -> tuple:
    """Filter key rows whose metadata.tags match any of the given patterns.

    Returns (named_aliases, unnamed_count).
    """

    affected: list = []
    unnamed_count = 0
    for key in keys:
        key_alias = key.key_alias or ""
        key_tags = _get_tags_from_metadata(
            key.metadata, getattr(key, "metadata_json", None)
        )
        if key_tags and any(
            RouteChecks._route_matches_wildcard_pattern(route=tag, pattern=pat)
            for tag in key_tags
            for pat in tag_patterns
        ):
            if key_alias:
                affected.append(key_alias)
            else:
                unnamed_count += 1
    return affected, unnamed_count

