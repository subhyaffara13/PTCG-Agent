
def angle_impl(self: ComplexTensor) -> torch.Tensor:
    x, y = split_complex_tensor(self)
    return torch.atan2(y, x)

