
def _find_node(gm: torch.fx.GraphModule, name: str) -> torch.fx.Node:
    return next(iter(node for node in gm.graph.nodes if node.name == name))

