
def is_probably_private(name: str) -> bool:
    return name.startswith("_") and not is_dunder(name)

