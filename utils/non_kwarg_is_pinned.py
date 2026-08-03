from typing import Any

def non_kwarg_is_pinned(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> bool:
    _, new_kwargs = _normalize_function_or_error(
        func, args, kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")
    # we'll ignore device argument because it is deprecated and not
    # actually used by is_pinned.
    with in_kernel_invocation_manager(fake_mode):
        r = func(inp)
    return r

