
def get_nodes_with_chunking_meta(graph: torch.fx.Graph) -> Sequence[Node]:
    from .core import get_chunking_meta

    output = []
    for node in graph.nodes:
        if get_chunking_meta(node):
            output.append(node)
    return output

