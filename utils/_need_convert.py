
def _need_convert(kind: str) -> bool:
    if kind in ("datetime64", "string") or "datetime64" in kind:
        return True
    return False

