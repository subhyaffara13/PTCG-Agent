
def _prelu_kernel(self: Tensor, weight: Tensor) -> Tensor:
    return torch.where(self > 0, self, weight * self)

