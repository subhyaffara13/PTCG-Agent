
def has_same_parent_node(node: torch.fx.Node):
    # the input nodes of the node should come from the same parent
    prev_node = None
    for getitem in node.args[0]:  # type: ignore[union-attr]
        if getitem.target != operator.getitem:  # type: ignore[union-attr]
            return False
        if prev_node is None:
            prev_node = getitem.args[0]  # type: ignore[union-attr]
        else:
            if getitem.args[0] != prev_node:  # type: ignore[union-attr]
                return False
    return True

