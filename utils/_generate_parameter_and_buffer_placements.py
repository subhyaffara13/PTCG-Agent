
def _generate_parameter_and_buffer_placements(
    params_and_buffers: list[str],
    parallel_strategies: dict[str, ParallelStyle],
) -> dict[str, Placement]:
    """
    Build parameter placements based on the give parallel style of linear layers.
    """
    parameter_placements: dict[str, Placement] = {}
    for linear_fqn, parallel_style in parallel_strategies.items():
        weight_fqn = f"{linear_fqn}.weight"
        bias_fqn = f"{linear_fqn}.bias"
        if weight_fqn not in params_and_buffers:
            raise AssertionError
        parameter_placements[weight_fqn] = (
            Shard(0) if parallel_style == ColwiseParallel else Shard(1)
        )
        if bias_fqn in params_and_buffers:
            parameter_placements[bias_fqn] = (
                Shard(0) if parallel_style == ColwiseParallel else Replicate()
            )
    return parameter_placements

