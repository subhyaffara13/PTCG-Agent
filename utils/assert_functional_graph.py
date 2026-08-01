
def assert_functional_graph(fx_g: torch.fx.Graph) -> int:
    error, mutation_count = _is_functional_graph(fx_g)
    if error is not None:
        raise AssertionError(error)
    return mutation_count

