
def _find_hop_subgraph_outputs(gm: torch.fx.GraphModule) -> tuple[torch.fx.Node]:
    output_node_args = gm.graph.find_nodes(op="output")[0].args
    if not isinstance(output_node_args, tuple):
        raise AssertionError(
            f"expected output_node_args to be tuple, got {type(output_node_args)}"
        )
    return output_node_args[0]

