
def _graph_input_names(gm: torch.fx.GraphModule) -> list[str]:
    return [node.name for node in gm.graph.find_nodes(op="placeholder")]

