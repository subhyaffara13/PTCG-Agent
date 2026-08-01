
def _matches_filters(job_properties: dict[str, str], filters: list[tuple[str, str, str]]) -> bool:
    """Check if scheduled job matches all specified filters."""
    for key, op_str, pattern in filters:
        value = job_properties.get(key)
        if value is None:
            if op_str == "!=":
                continue
            return False
        match = fnmatch(value.lower(), pattern.lower())
        if (op_str == "=" and not match) or (op_str == "!=" and match):
            return False
    return True

