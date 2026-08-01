
def _is_before(node: nodes.NodeNG, reference_node: nodes.NodeNG) -> bool:
    """Checks if node appears before reference_node."""
    if node.lineno < reference_node.lineno:
        return True
    if (
        node.lineno == reference_node.lineno
        and node.col_offset < reference_node.col_offset
    ):
        return True
    return False

