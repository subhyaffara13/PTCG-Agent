from typing import Any, Callable

def get_default_arg_names(function: Callable[..., Any]) -> tuple[str, ...]:
    # Note: this code intentionally mirrors the code at the beginning of
    # getfuncargnames, to get the arguments which were excluded from its result
    # because they had default values.
    return tuple(
        p.name
        for p in signature(function).parameters.values()
        if p.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        and p.default is not Parameter.empty
    )

