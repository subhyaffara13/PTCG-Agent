
def _param_groups_val_list(optimizer: Optimizer, key: str) -> list[Any]:
    """Create a list containing group[key] for each optimizer param_group.
    Prevents aliasing when group[key] could be a Tensor.
    Raises a KeyError when group[key] does not exist.
    """
    return [
        group[key].clone() if isinstance(group[key], Tensor) else group[key]
        for group in optimizer.param_groups
    ]

