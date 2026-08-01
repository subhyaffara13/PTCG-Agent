
def use_autoheuristic(name: str) -> bool:
    if name == "pad_mm":
        return autoheuristic_use.pad_mm
    elif name == "mixed_mm":
        return autoheuristic_use.mixed_mm
    else:
        # For test compatibility with non-standard ops (e.g. "test", "foo" used in tests)
        return name in _parse_autoheuristic_use_env()

