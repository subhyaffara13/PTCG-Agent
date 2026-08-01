
def _normalize_name(name: str) -> str:
    return _NORMALIZE_PATTERN.sub("-", name).lower()


def _normalize_name(name: str) -> str:
    """Make a name consistent regardless of source (environment or file)"""
    name = name.lower().replace("_", "-")
    name = name.removeprefix("--")  # only prefer long opts
    return name


def _normalize_name(name: str) -> str:
    return _NORMALIZE_PATTERN.sub("-", name).lower()

