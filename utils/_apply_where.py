from typing import Callable

def _apply_where(  # numpydoc ignore=PR01,RT01
    cond: Array,
    f1: Callable[..., Array],
    f2: Callable[..., Array] | None,
    fill_value: Array | int | float | complex | bool | None,
    *args: Array,
    kwkeys: list[str],
    xp: ModuleType,
) -> Array:
    """Helper of `apply_where`. On Dask, this runs on a single chunk."""

    nargs = len(args) - len(kwkeys)
    kwargs = dict(zip(kwkeys, args[nargs:], strict=True))
    args = args[:nargs]

    if not capabilities(xp, device=_compat.device(cond))["boolean indexing"]:
        # jax.jit does not support assignment by boolean mask
        return xp.where(
            cond,
            f1(*args, **kwargs),
            f2(*args, **kwargs) if f2 is not None else fill_value,
        )

    temp1 = f1(
        *(arr[cond] for arr in args), **{key: val[cond] for key, val in kwargs.items()}
    )

    if f2 is None:
        dtype = xp.result_type(temp1, fill_value)
        if isinstance(fill_value, int | float | complex):
            out = xp.full_like(cond, dtype=dtype, fill_value=fill_value)
        else:
            out = xp.astype(fill_value, dtype, copy=True)
    else:
        ncond = ~cond
        temp2 = f2(
            *(arr[ncond] for arr in args),
            **{key: val[ncond] for key, val in kwargs.items()},
        )
        dtype = xp.result_type(temp1, temp2)
        out = xp.empty_like(cond, dtype=dtype)
        out = at(out, ncond).set(temp2)

    return at(out, cond).set(temp1)

