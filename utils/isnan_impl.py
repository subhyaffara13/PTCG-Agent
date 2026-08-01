
def isnan_impl(self: ComplexTensor) -> torch.Tensor:
    re, im = split_complex_tensor(self)
    return torch.isnan(re) | torch.isnan(im)

