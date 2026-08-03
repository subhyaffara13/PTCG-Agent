from typing import Any

def _trace_wrapped_op_dense(*args: Any, fn: Any, **kwargs: Any) -> Any:
    mode = _get_current_dispatch_mode()
    assert mode is None, "Mode should never be enabled for CPU/CUDA key"
    return fn(*args, **kwargs)

