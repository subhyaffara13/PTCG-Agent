
def cos_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    return torch.cosh(ComplexTensor(-y, x))  # type: ignore[bad-return]

