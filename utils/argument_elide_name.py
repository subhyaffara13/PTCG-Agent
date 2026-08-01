
def argument_elide_name(name: str | None) -> bool:
    return name is not None and name.startswith("__") and not name.endswith("__")

