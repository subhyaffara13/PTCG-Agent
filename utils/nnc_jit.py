from typing import Any, Callable

def nnc_jit(f: Callable[..., Any]) -> Callable[..., Any]:
    return aot_function(f, simple_ts_compile)

