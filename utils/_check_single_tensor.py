
def _check_single_tensor(param, param_name: str) -> None:
    """Check that the parameter ``param_name`` is a single tensor."""
    if not isinstance(param, torch.Tensor):
        raise TypeError(
            f"""Invalid function argument. Expected parameter `{param_name}` of type torch.Tensor
             but got {type(param)} instead."""
        )

