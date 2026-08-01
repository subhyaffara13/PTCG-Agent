
def maybe_disable_graph_partition(
    cpp_wrapper: bool, aot_mode: bool
) -> AbstractContextManager[None, None]:
    """
    graph partition does not support cpp_wrapper and aot_mode yet.
    """
    if cpp_wrapper or aot_mode:
        return config.patch(graph_partition=False)
    else:
        return contextlib.nullcontext()

