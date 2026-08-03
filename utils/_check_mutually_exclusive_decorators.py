from typing import Callable

def _check_mutually_exclusive_decorators(fn: Callable, decorator_name: str) -> None:
    mutually_exclusive = {
        "leaf_function": trace_rules.is_leaf_function,
        "nonstrict_trace": trace_rules.is_nonstrict_trace_callable,
    }

    for other_name, check_fn in mutually_exclusive.items():
        if other_name != decorator_name and check_fn(fn):
            first, second = sorted([decorator_name, other_name])
            raise ValueError(
                f"Function {fn} cannot be both marked as @{first} and "
                f"@{second}. Please use only one decorator."
            )

