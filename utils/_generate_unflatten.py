
def _generate_unflatten(
    gm: torch.fx.GraphModule | InterpreterModule | UnflattenedModule, nodes, spec
) -> torch.fx.Node:
    name = _add_spec(gm, spec)
    spec_node = gm.graph.get_attr(name)
    return gm.graph.call_function(pytree.tree_unflatten, (nodes, spec_node))

