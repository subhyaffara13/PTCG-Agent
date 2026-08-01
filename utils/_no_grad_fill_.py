
def _no_grad_fill_(tensor: Tensor, val: float) -> Tensor:
    with torch.no_grad():
        return tensor.fill_(val)

