
def stop():
    r"""Stops cuda profiler data collection.

    .. warning::
        Raises CudaError in case of it is unable to stop the profiler.
    """
    check_error(cudart().cudaProfilerStop())


def stop() -> None:
    r"""Stops generating OS Signpost tracing from MPS backend."""
    torch._C._mps_profilerStopTrace()  # type: ignore[attr-defined]

