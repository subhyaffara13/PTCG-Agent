
def is_blacklisted_path(path: str) -> bool:
    return any(substr in (normalize_path_separators(path) + "\n") for substr in BLACKLIST)

