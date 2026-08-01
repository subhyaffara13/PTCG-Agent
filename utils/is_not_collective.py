
def is_not_collective(node: fx.Node) -> bool:
    return getattr(node.target, "namespace", None) != "_c10d_functional"

