
def _get_break_loop_node(break_node: nodes.Break) -> nodes.For | nodes.While | None:
    """Returns the loop node that holds the break node in arguments.

    Args:
        break_node (nodes.Break): the break node of interest.

    Returns:
        nodes.For or nodes.While: the loop node holding the break node.
    """
    loop_nodes = (nodes.For, nodes.While)
    parent = break_node.parent
    while not isinstance(parent, loop_nodes) or break_node in getattr(
        parent, "orelse", []
    ):
        break_node = parent
        parent = parent.parent
        if parent is None:
            break
    return parent

