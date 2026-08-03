from typing import Callable

def _wrap_graph_break_with_torch_runtime_err(gb_fn: Callable[[], NoReturn]) -> NoReturn:
    from .exc import TorchRuntimeError, Unsupported

    try:
        gb_fn()
    except Unsupported as e:
        exc = TorchRuntimeError(str(e), getattr(e, "real_stack", None))
        raise exc.with_traceback(e.__traceback__) from None
    raise AssertionError("should be unreachable")

