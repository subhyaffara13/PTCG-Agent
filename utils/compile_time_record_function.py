from typing import Any

def compile_time_record_function(name: str) -> Generator[Any, None, None]:
    """
    A context manager for compile-time profiling that uses _RecordFunctionFast
    for lower overhead than torch.profiler.record_function.

    This is intended for use during compilation (dynamo, inductor, etc.) where
    we want profiling support but with minimal overhead. Moreover, we do not
    want the record_function call inside torch.compile to be dispatched.

    Args:
        name: The name of the record function event that will appear in profiles.
    """
    if torch.autograd.profiler._is_profiler_enabled:
        rf = torch._C._profiler._RecordFunctionFast(name)
        rf.__enter__()
        try:
            yield
        finally:
            rf.__exit__(None, None, None)
    else:
        yield

