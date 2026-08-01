
def get_custom_estimation(
    n: fx.Node,
    custom_runtime_estimation: Callable[[fx.Node, int | None], float | None]
    | None = None,
    override_size: int | None = None,
) -> float | None:
    if custom_runtime_estimation is None:
        return None

    return custom_runtime_estimation(n, override_size)

