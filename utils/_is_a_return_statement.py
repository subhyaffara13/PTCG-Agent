
def _is_a_return_statement(node: nodes.Call) -> bool:
    frame = node.frame()
    for parent in node.node_ancestors():
        if parent is frame:
            break
        if isinstance(parent, nodes.Return):
            return True
    return False

