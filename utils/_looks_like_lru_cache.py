
def _looks_like_lru_cache(node) -> bool:
    """Check if the given function node is decorated with lru_cache."""
    if not node.decorators:
        return False
    for decorator in node.decorators.nodes:
        if not isinstance(decorator, (nodes.Attribute, nodes.Call)):
            continue
        if _looks_like_functools_member(decorator, "lru_cache"):
            return True
    return False

