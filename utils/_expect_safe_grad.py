
def _expect_safe_grad(t: _TensorLikeT) -> _TensorLikeT:
    grad = safe_grad(t)
    if grad is None:
        raise AssertionError("Expected tensor to have a gradient but grad is None")
    return grad

