
def _update_param_group_val(
    param_group: dict[str, Any], key: str, val: float | Tensor
) -> None:
    """Set param_group[key] to val without aliasing or assignment when they're
    both tensors. Raises a KeyError if param_group[key] does not exist.
    """
    if isinstance(param_group[key], Tensor):
        param_group[key].fill_(_to_scalar(val))
    else:
        param_group[key] = val

