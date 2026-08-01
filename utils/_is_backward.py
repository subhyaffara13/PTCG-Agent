
def _is_backward(graph: torch.fx.Graph) -> bool:
    placeholders = []
    for node in graph.nodes:
        if node.op != "placeholder":
            break
        placeholders.append(node)
    return not all(node.name.startswith("primal") for node in placeholders)

