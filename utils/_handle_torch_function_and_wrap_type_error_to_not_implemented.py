import functools
from typing import Callable

def _handle_torch_function_and_wrap_type_error_to_not_implemented(
    f: Callable[Concatenate[_TensorLike, _P], "Tensor"],
) -> Callable[Concatenate[_TensorLike, _P], "Tensor"]:
    @functools.wraps(f)
    def wrapped(self: _TensorLike, *args: _P.args, **kwargs: _P.kwargs) -> "Tensor":
        try:
            # See https://github.com/pytorch/pytorch/issues/75462
            sargs = self, *args
            if has_torch_function(sargs):
                return handle_torch_function(wrapped, sargs, self, *args, **kwargs)
            return f(self, *args, **kwargs)
        except TypeError:
            return NotImplemented

    return wrapped

