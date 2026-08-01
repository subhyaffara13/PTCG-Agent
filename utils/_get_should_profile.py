
def _get_should_profile():
    # Legacy profiler should be enabled. RPC profiling is not supported with
    # Kineto profiler.
    ActiveProfilerType = torch._C._profiler.ActiveProfilerType
    return (
        torch.autograd._profiler_enabled()
        and torch._C._autograd._profiler_type() == ActiveProfilerType.LEGACY  # type: ignore[attr-defined]
    )

