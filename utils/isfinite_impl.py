
def isfinite_impl(self: ComplexTensor) -> torch.Tensor:
    re, im = split_complex_tensor(self)
    return torch.isfinite(re) & torch.isfinite(im)

