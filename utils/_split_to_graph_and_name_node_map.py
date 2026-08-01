
def _split_to_graph_and_name_node_map(
    gm: GraphModule,
) -> tuple[GraphModule, dict[str, Node]]:
    from torch.fx.graph import _PyTreeInfo
    from torch.utils._pytree import tree_flatten, tree_unflatten

    name_node_map = {}
    for n in gm.graph.nodes:
        if n.op == "output":
            if gm._out_spec is None:
                raise AssertionError("gm._out_spec is None")
            output = tree_unflatten(n.args[0], gm._out_spec)
            if not isinstance(output, tuple):
                raise AssertionError("Expecting the pattern graph to return a tuple")
            if len(output) < 2:
                raise AssertionError(
                    "Expecting the pattern graph to have at least two outputs"
                )
            *out, name_node_map = output
            flattened, out_spec = tree_flatten(out)
            if not isinstance(name_node_map, dict):
                raise AssertionError(
                    "Expecting the input graph to have a dict output as the last element"
                )
            n.args = (flattened,)
            orig_pytree_info = gm._graph._codegen.pytree_info  # type: ignore[attr-defined]
            gm._graph._codegen.pytree_info = _PyTreeInfo(  # type: ignore[attr-defined]
                orig_pytree_info.orig_args, orig_pytree_info.in_spec, out_spec
            )
    gm.recompile()
    return gm, name_node_map

