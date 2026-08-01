
def is_typevar_default_recursive(tv_fname: str, start: TypeInfo | TypeAlias) -> bool:
    """Check if the type variable can lead to infinite recursion via defaults."""
    if tv_fname not in start.default_depends:
        return False
    todo = start.default_depends[tv_fname].copy()
    seen: set[TypeAlias | TypeInfo] = set()
    while todo:
        node = todo.pop()
        if node is start:
            return True
        if node in seen:
            # We don't return True here, since we are interested only in
            # recursion via the original type variable.
            continue
        seen.add(node)
        for dep_nodes in node.default_depends.values():
            todo |= dep_nodes
    return False

