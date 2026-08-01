
def has_underscore_prefix(name: str) -> bool:
    return name.startswith("_") and not (name.startswith("__") and name.endswith("__"))

