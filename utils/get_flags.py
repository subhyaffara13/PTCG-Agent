
def get_flags(node: Node, names: list[str]) -> list[str]:
    return [name for name in names if getattr(node, name)]

