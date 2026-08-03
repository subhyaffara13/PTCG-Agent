from typing import Any, Callable

def _lazy_apply_wrapper(  # numpydoc ignore=PR01,RT01
    func: Callable[..., Array | ArrayLike | Sequence[Array | ArrayLike]],
    as_numpy: bool,
    multi_output: bool,
    xp: ModuleType,
) -> Callable[..., tuple[Array, ...]]:
    """
    Helper of `lazy_apply`.

    Given a function that accepts one or more arrays as positional arguments and returns
    a single array-like or a sequence of array-likes, return a function that accepts the
    same number of Array API arrays and always returns a tuple of Array API array.

    Any keyword arguments are passed through verbatim to the wrapped function.
    """

    # On Dask, @wraps causes the graph key to contain the wrapped function's name
    @wraps(func)
    def wrapper(
        *args: Array | complex | None, **kwargs: Any
    ) -> tuple[Array, ...]:  # numpydoc ignore=GL08
        args_list = []
        device = None
        for arg in args:
            if arg is not None and not is_python_scalar(arg):
                if device is None:
                    device = _compat.device(arg)
                if as_numpy:
                    import numpy as np

                    arg = cast(Array, np.asarray(arg))  # pyright: ignore[reportInvalidCast] # noqa: PLW2901
            args_list.append(arg)
        assert device is not None

        out = func(*args_list, **kwargs)

        if multi_output:
            assert isinstance(out, Sequence)
            return tuple(xp.asarray(o, device=device) for o in out)
        return (xp.asarray(out, device=device),)

    return wrapper

