
def _generate_flatten_spec(
    gm: torch.fx.GraphModule | InterpreterModule | UnflattenedModule, node, spec
) -> torch.fx.Node:
    name = _add_spec(gm, spec)
    spec_node = gm.graph.get_attr(name)
    return gm.graph.call_function(fx_pytree.tree_flatten_spec, (node, spec_node))

