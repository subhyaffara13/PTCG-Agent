
def short_name(name: str) -> str:
    if name.startswith("builtins."):
        return name[9:]
    return name

