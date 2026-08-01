
def is_graph_input(node: torch.fx.Node) -> bool:
    return node.op == "placeholder"

