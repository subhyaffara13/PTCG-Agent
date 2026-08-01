
def _check_tensor_all_with(error_type, cond, message=None):  # noqa: F811
    if not is_tensor(cond):
        raise TypeError(f"cond must be a tensor, but got {type(cond)}")

    if not cond.dtype == torch.bool:
        raise TypeError(f"cond tensor must have dtype torch.bool, but got {cond.dtype}")

    _check_with(error_type, cond._is_all_true().item(), message)  # type: ignore[arg-type]

