
def _remove_by_pattern(paths: set[str], exclude_patterns: set[str]) -> None:
    for pattern in exclude_patterns:
        paths.difference_update(fnmatch.filter(paths, pattern))

