
def _unquote_path_safe(value: str) -> str:
    if "%" not in value:
        return value
    return value.replace("%2F", "/").replace("%25", "%")

