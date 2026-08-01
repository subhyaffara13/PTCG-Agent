
def imag_impl(self: ComplexTensor) -> torch.Tensor:
    _, im = split_complex_tensor(self)
    return im

