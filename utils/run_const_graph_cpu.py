
def run_const_graph_cpu(
    graph: torch.fx.GraphModule, args: tuple[object, ...]
) -> object:
    if not isinstance(graph, torch.fx.GraphModule):
        raise AssertionError(
            f"expected graph to be torch.fx.GraphModule, got {type(graph)}"
        )
    return graph(*args)

