
def _detach_if_needed(param_or_tensor: nn.Parameter | Tensor) -> Tensor:
    return (
        param_or_tensor.detach()
        if isinstance(param_or_tensor, nn.Parameter)
        else param_or_tensor
    )

