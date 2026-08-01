
def _safe_attr_access(var: str, attr: str) -> str:
    if attr.isidentifier() and not keyword.iskeyword(attr):
        return f"{var}.{attr}"
    return f"getattr({var}, {attr!r})"

