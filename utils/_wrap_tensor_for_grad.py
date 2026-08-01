
def _wrap_tensor_for_grad(maybe_tensor: _T, level: int) -> _T:
    if not isinstance(maybe_tensor, torch.Tensor):
        return maybe_tensor
    # pyrefly: ignore[bad-return]
    return _wrap_for_grad(maybe_tensor, level)

