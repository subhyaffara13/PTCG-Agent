from typing import Callable

def _inplace_wrapper(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    """
    Given a nn.functional non-linearity, implements its `inplace: bool` argument
    """

    # nb. We use the name of the first argument used in the unary references
    @wraps(fn)
    def _fn(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        a = args[0]
        if "inplace" not in kwargs:
            kwargs["inplace"] = False

        if kwargs["inplace"]:
            torch._check(
                "out" not in kwargs,
                lambda: "Cannot set inplace=True and pass out= at the same time",
            )
            kwargs["inplace"] = False
            kwargs["out"] = a
            return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)

    return _fn

