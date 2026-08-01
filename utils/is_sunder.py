
def is_sunder(name: str) -> bool:
    return not is_dunder(name) and name.startswith("_") and name.endswith("_") and name != "_"

