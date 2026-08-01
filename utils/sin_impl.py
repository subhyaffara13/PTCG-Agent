
def sin_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    sinh_iz = torch.sinh(ComplexTensor(-y, x))
    if not isinstance(sinh_iz, ComplexTensor):
        raise AssertionError(f"sinh_iz must be a ComplexTensor, got {type(sinh_iz)}")
    sinh_iz_re, sinh_iz_im = split_complex_tensor(sinh_iz)
    return ComplexTensor(sinh_iz_im, -sinh_iz_re)

