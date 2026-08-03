from typing import Callable

def elementwise_unary_scalar_wrapper(
    fn: Callable[_P, _T],
) -> Callable[_P, _T | NumberType]:
    """
    Allows unary operators that accept tensors to work with Python numbers.
    """
    sig = inspect.signature(fn)

    @wraps(fn)
    def _fn(*args, **kwargs):
        if len(args) > 0 and isinstance(args[0], Number):
            dtype = utils.type_to_dtype(type(args[0]))
            args_ = list(args)
            args_[0] = torch.tensor(args[0], dtype=dtype)
            # pyrefly: ignore [invalid-param-spec]
            result = fn(*args_, **kwargs)
            if not isinstance(result, torch.Tensor):
                raise AssertionError(f"Expected torch.Tensor, got {type(result)}")
            return result.item()

        # pyrefly: ignore [invalid-param-spec]
        return fn(*args, **kwargs)

    _fn.__signature__ = sig  # type: ignore[attr-defined]
    # pyrefly: ignore [bad-return]
    return _fn

