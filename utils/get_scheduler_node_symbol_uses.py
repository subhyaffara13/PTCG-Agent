
def get_scheduler_node_symbol_uses(
    node: BaseSchedulerNode,
) -> OrderedSet[sympy.Symbol]:
    """
    Gets symbols used in a scheduler node, including free symbols from
    the node's operations and layout symints from outputs.
    """
    if isinstance(node, FusedSchedulerNode):
        return OrderedSet().union(
            *(get_scheduler_node_symbol_uses(snode) for snode in node.snodes)
        )
    assert node.node is not None
    free_symbol_uses = node.node.get_free_symbol_uses()
    free_symbol_uses.update(
        *(get_layout_symints(ir_node) for ir_node in node.node.get_outputs())
    )
    return free_symbol_uses

