from typing import Callable

def _unsqueeze_atleast(
    at_least_fn: Callable, dim: int, arg: TensorLikeType
) -> TensorLikeType:
    arg_ = at_least_fn(arg)
    if not isinstance(arg_, TensorLike):
        raise AssertionError(f"at_least_fn must return TensorLike, got {type(arg_)}")
    return unsqueeze(arg_, dim)

