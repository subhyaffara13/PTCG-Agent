
def run_const_graph_fake_tensor_mode(
    mode: FakeTensorMode, graph: torch.fx.GraphModule, args: tuple[object, ...]
) -> object:
    if not isinstance(graph, torch.fx.GraphModule):
        raise AssertionError(
            f"expected graph to be torch.fx.GraphModule, got {type(graph)}"
        )
    with mode:
        return graph(*args)

