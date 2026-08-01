
def doesnt_support_saved_tensors_hooks(f: Callable[_P, _R]) -> Callable[_P, _R]:
    message = (
        "torch.func.{grad, vjp, jacrev, hessian} don't yet support saved tensor hooks. "
        "Please open an issue with your use case."
    )

    @functools.wraps(f)
    def fn(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        with torch.autograd.graph.disable_saved_tensors_hooks(message):
            return f(*args, **kwargs)

    return fn

