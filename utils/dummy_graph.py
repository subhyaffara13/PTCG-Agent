
def dummy_graph() -> GraphLowering:
    """
    Create a graph. This is useful for unit testing code which accesses
    V.graph.sizevars.
    """
    example_inputs = [torch.randn(10) for _ in range(2)]
    gm = make_fx(torch.add, tracing_mode="fake")(*example_inputs)
    shape_env = shape_env_from_inputs(example_inputs)
    graph = GraphLowering(
        gm,
        shape_env=shape_env,
    )

    return graph

