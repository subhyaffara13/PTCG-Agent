
def _no_grad(func: Callable[_P, _R]) -> Callable[_P, _R]:
    """
    This wrapper is needed to avoid a circular import when using @torch.no_grad on the exposed functions
    clip_grad_norm_ and clip_grad_value_ themselves.
    """

    def _no_grad_wrapper(*args, **kwargs):
        with torch.no_grad():
            return func(*args, **kwargs)

    functools.update_wrapper(_no_grad_wrapper, func)
    # pyrefly: ignore [bad-return]
    return _no_grad_wrapper

