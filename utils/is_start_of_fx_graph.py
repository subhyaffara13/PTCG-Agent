
def is_start_of_fx_graph(graph: torch.fx.Graph, node: torch.fx.Node) -> bool:
    # first node in the graph
    return node is next(iter(graph.nodes))

