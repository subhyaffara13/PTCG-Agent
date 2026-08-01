
def _is_housekeeping_name(name: str) -> bool:
    return name.startswith(".") or _BREAK_SUFFIX in name

