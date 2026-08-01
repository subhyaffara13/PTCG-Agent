
def view_as_real_impl(self: ComplexTensor) -> torch.Tensor:
    re, im = split_complex_tensor(self)
    return torch.stack([re, im], dim=-1)

