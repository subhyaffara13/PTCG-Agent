
def estimate_collective_time(
    n: fx.Node,
    override_size: int | None = None,
    custom_runtime_estimation: Callable[[fx.Node, int | None], float | None]
    | None = None,
    collective_estimator: Literal["analytical", "benchmark"] = "analytical",
) -> float:
    """Estimate the runtime of a collective operation, optionally with an overridden size."""
    if (
        est := get_custom_estimation(n, custom_runtime_estimation, override_size)
    ) is not None:
        return est

    if collective_estimator == "benchmark":
        from torch._inductor.fx_passes.node_runtime_estimation import (
            benchmark_collective_with_cuda_events,
        )

        cuda_val, _ = benchmark_collective_with_cuda_events(n, nruns=5)
        if cuda_val is not None:
            return cuda_val

    # Analytical model (also fallback when benchmark returns None)
    return torch._inductor.comm_analysis.estimate_nccl_collective_runtime_from_fx_node(
        n, override_size
    )

