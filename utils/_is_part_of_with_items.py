
def _is_part_of_with_items(node: nodes.Call) -> bool:
    """Checks if one of the node's parents is a ``nodes.With`` node and that the node
    itself is located somewhere under its ``items``.
    """
    frame = node.frame()
    current = node
    while current != frame:
        if isinstance(current, nodes.With):
            items_start = current.items[0][0].lineno
            items_end = current.items[-1][0].tolineno
            return items_start <= node.lineno <= items_end  # type: ignore[no-any-return]
        current = current.parent
    return False

