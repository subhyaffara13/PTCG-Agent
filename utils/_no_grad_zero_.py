
def _no_grad_zero_(tensor: Tensor) -> Tensor:
    with torch.no_grad():
        return tensor.zero_()

