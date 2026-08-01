
def _deprecated(name):
    warnings.warn(f"hipify version 2.0.0 no longer uses function {name}", FutureWarning, stacklevel=2)


def _deprecated(name, suggestion):
    warnings.warn(
        f"torch.distributed.nn.functional.{name} is deprecated, "
        f"use {suggestion} instead.",
        category=FutureWarning,
        stacklevel=3,
    )


def _deprecated(msg, stacklevel=2):
    """Deprecate a function by emitting a warning on use."""
    def wrap(fun):
        if isinstance(fun, type):
            warnings.warn(
                f"Trying to deprecate class {fun!r}",
                category=RuntimeWarning, stacklevel=2)
            return fun

        @functools.wraps(fun)
        def call(*args, **kwargs):
            warnings.warn(msg, category=DeprecationWarning,
                          stacklevel=stacklevel)
            return fun(*args, **kwargs)
        call.__doc__ = fun.__doc__
        return call

    return wrap

