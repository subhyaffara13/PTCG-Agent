
def collect_autoheuristic(name: str) -> bool:
    if name == "pad_mm":
        return autoheuristic_collect.pad_mm
    elif name == "mixed_mm":
        return autoheuristic_collect.mixed_mm
    else:
        # For test compatibility with non-standard ops (e.g. "test", "foo" used in tests)
        return name in _parse_autoheuristic_collect_env()

