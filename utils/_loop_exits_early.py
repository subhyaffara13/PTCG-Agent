
def _loop_exits_early(loop: nodes.For | nodes.While) -> bool:
    """Returns true if a loop may end with a break statement.

    Args:
        loop (nodes.For, nodes.While): the loop node inspected.

    Returns:
        bool: True if the loop may end with a break statement, False otherwise.
    """
    loop_nodes = (nodes.For, nodes.While)
    definition_nodes = (nodes.FunctionDef, nodes.ClassDef)
    inner_loop_nodes: list[nodes.For | nodes.While] = [
        _node
        for _node in loop.nodes_of_class(loop_nodes, skip_klass=definition_nodes)
        if _node != loop
    ]
    return any(
        _node
        for _node in loop.nodes_of_class(nodes.Break, skip_klass=definition_nodes)
        if _get_break_loop_node(_node) not in inner_loop_nodes
    )

