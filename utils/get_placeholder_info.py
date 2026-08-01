
def get_placeholder_info(graph: torch.fx.Graph) -> list[PlaceholderInfo]:
    return [
        to_placeholder_info(node) for node in graph.nodes if node.op == "placeholder"
    ]

