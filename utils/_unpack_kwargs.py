from typing import Any

def _unpack_kwargs(
    flat_args: tuple[Any, ...], kwarg_keys: tuple[str, ...]
) -> tuple[tuple[Any, ...], dict[str, Any]]:
    """See _pack_kwargs."""
    if len(kwarg_keys) > len(flat_args):
        raise AssertionError(f"too many keys {len(kwarg_keys)} vs. {len(flat_args)}")
    if len(kwarg_keys) == 0:
        return flat_args, {}
    args = flat_args[: -len(kwarg_keys)]
    kwargs = dict(zip(kwarg_keys, flat_args[-len(kwarg_keys) :]))
    return args, kwargs

