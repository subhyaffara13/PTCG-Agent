
def _resolve_inductor_callable(
    func: int | InductorCompiledCallable,
) -> InductorCompiledCallable:
    """
    Resolve func to an InductorCompiledCallable.

    func is either an InductorCompiledCallable directly (from post_compile)
    or an int index into the side table (from a traced FX graph node).
    """
    if isinstance(func, int):
        return inductor_code_side_table.get_callable(func)
    assert isinstance(func, InductorCompiledCallable), (  # noqa: S101
        f"Unexpected func type: {type(func)}"
    )
    return func

