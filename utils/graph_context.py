
def graph_context() -> Generator[None, None, None]:
    """
    Wrapped around processing a graph, sets up figuring out which ranks tune
    which shapes.
    """
    assert not isinstance(
        V.get_distributed_autotune_state(check_poisoned=False),  # type: ignore[call-arg]
        _DistributedAutotuneState,
    )
    V.set_distributed_autotune_state(_DistributedAutotuneState())
    try:
        yield
    finally:
        V.set_distributed_autotune_state(NullHandler())

