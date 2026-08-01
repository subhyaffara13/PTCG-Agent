
def launch_(
    grid_size: Tuple[Any, Any, Any],
    block_size: Tuple[Any, Any, Any],
    async_dependencies=None,
    dynamic_shared_memory_size: Optional[Value] = None,
    *,
    loc=None,
    ip=None,
):
    grid_size = tuple(map(_convert_literal_to_constant, grid_size))
    block_size = tuple(map(_convert_literal_to_constant, block_size))
    launch_op = LaunchOp(
        grid_size,
        block_size,
        async_dependencies,
        dynamic_shared_memory_size,
        loc=loc,
        ip=ip,
    )
    return launch_op

