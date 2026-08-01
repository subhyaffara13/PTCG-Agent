
def safe_grad(t: _TensorLikeT) -> _TensorLikeT | None:
    with torch._logging.hide_warnings(torch._logging._internal.safe_grad_filter):
        # pyrefly: ignore [bad-return]
        return t.grad

