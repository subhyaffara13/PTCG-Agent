
def _generate_flatten(gm: torch.fx.GraphModule, node) -> torch.fx.Node:
    flatten = gm.graph.call_function(pytree.tree_flatten, (node,))
    getitem_0 = gm.graph.call_function(operator.getitem, (flatten, 0))
    return getitem_0

