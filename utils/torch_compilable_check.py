import os
from typing import Any, Callable

def torch_compilable_check(cond: Any, msg: str | Callable[[], str], error_type: type[Exception] = ValueError) -> None:
    """
    Combines the functionalities of `torch._check`, `torch._check_with` and `torch._check_tensor_all_with` to provide a
    unified way to perform checks that are compatible with TorchDynamo (torch.compile & torch.export).

    The advantage of using `torch._check(cond, msg, error_type)` over `if cond: raise error_type(msg)` is that the former
    works as a truthfulness hint for TorchDynamo, instead of failing with a data-dependent control flow error during compilation.

    All checks using this method can be disabled in production environments by setting `TRANSFORMERS_DISABLE_TORCH_CHECK=1`.

    Args:
        cond (`bool`, `torch.Tensor` or `Callable[[], bool | torch.Tensor]`): The condition to check.
        msg (`str` or `Callable[[], str]`): The error message to display if the condition is not met.
        error_type (`type[Exception]`, *optional*, defaults to `ValueError`): The type of error to raise if the condition is not met.

    Raises:
        error_type: If the condition is not met.
    """
    if os.getenv("TRANSFORMERS_DISABLE_TORCH_CHECK", "0") == "1":
        return

    import torch

    # When tracing, msg may be an f-string with tensor values that dynamo can't trace
    # (callable/isinstance on it breaks). Check compilation first and use torch._check
    # without msg (it only serves as a compiler hint in that case).
    if is_tracing():
        if isinstance(cond, torch.Tensor):
            torch._check_tensor_all(cond)
        else:
            torch._check(cond)
        return

    if not callable(msg):
        # torch._check requires msg to be a callable but we want to keep the API simple for users
        def msg_callable():
            return msg
    else:
        msg_callable = msg

    if callable(cond):
        cond = cond()

    # These checks are also compiler hints for TorchDynamo telling
    # it that the condition is expected to be True during compilation
    if isinstance(cond, torch.Tensor):
        torch._check_tensor_all_with(error_type, cond, msg_callable)
    else:
        torch._check_with(error_type, cond, msg_callable)

