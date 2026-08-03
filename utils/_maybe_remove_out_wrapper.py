from typing import Callable

def _maybe_remove_out_wrapper(fn: Callable):
    return inspect.unwrap(
        fn,
        stop=lambda f: not hasattr(f, "_torch_decompositions_out_wrapper"),
    )

