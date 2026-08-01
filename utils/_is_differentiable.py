
def _is_differentiable(maybe_tensor: object) -> bool:
    if not isinstance(maybe_tensor, torch.Tensor):
        return False
    return maybe_tensor.requires_grad

