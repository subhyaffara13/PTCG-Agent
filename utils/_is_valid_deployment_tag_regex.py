
def _is_valid_deployment_tag_regex(
    tag_regexes: List[str],
    header_strings: List[str],
) -> Optional[str]:
    """
    Test compiled regex patterns against "Header-Name: value" strings.

    Returns the first matching pattern string, or None if nothing matches.
    Compiles each pattern once (re's LRU cache) and logs invalid patterns once
    per pattern, not once per header string.
    """
    for pattern in tag_regexes:
        try:
            compiled = re.compile(pattern)
        except re.error:
            verbose_logger.warning("tag_regex: invalid pattern %r — skipping", pattern)
            continue
        for header_str in header_strings:
            if compiled.search(header_str):
                return pattern
    return None

