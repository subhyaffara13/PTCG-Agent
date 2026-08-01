
def _resolve_private_replace_to_public(node: nodes.Module) -> None:
    """In python/cpython@6f3c138, a _replace() method was extracted from
    replace(), and this indirection made replace() uninferable."""
    if "_replace" in node.locals:
        node.locals["replace"] = node.locals["_replace"]

