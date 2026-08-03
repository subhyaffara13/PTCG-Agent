from typing import Callable

def _maybe_wrap_with_numa_binding(
    func: Callable[_TParams, _TReturn],
    *,
    gpu_index: int,
    numa_options: NumaOptions | None,
) -> Callable[_TParams, _TReturn]:
    """
    Wraps a function to apply NUMA CPU binding before execution.

    This decorator applies NUMA CPU affinity to all threads in the current process
    before calling the wrapped function, binding them to CPUs associated with the
    specified GPU's NUMA node.

    Args:
        func: The function to wrap with NUMA binding.
        gpu_index: The index of the GPU that will be used.
        numa_options: Configuration for NUMA binding behavior. If None, returns
            the original function unchanged.

    Returns:
        A wrapped function that applies NUMA binding before execution, or the
        original function if numa_options is None.
    """
    if numa_options is None:
        return func

    @wraps(func)
    def wrapped(*args: _TParams.args, **kwargs: _TParams.kwargs) -> _TReturn:
        _maybe_apply_numa_binding_to_current_process(
            gpu_index=gpu_index,
            # pyrefly: ignore [bad-argument-type]
            numa_options=numa_options,
        )
        return func(*args, **kwargs)

    return wrapped

