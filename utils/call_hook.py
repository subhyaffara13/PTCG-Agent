
def call_hook(
    hook: Callable[..., torch.Tensor | None], *args: Any, **kwargs: Any
) -> torch.Tensor:
    """
    Used by compiled autograd to handle hook returning None.
    """
    result = hook(*args)
    if result is None:
        return args[0]
    elif kwargs.get("hook_type") == "post_acc_grad_hook":
        raise RuntimeError("Tensor post accumulate grad hooks should return None.")
    return result

