
def atan_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    tanh_iz = torch.atanh(ComplexTensor(-y, x))
    if not isinstance(tanh_iz, ComplexTensor):
        raise AssertionError(f"tanh_iz must be a ComplexTensor, got {type(tanh_iz)}")
    tanh_iz_re, tanh_iz_im = split_complex_tensor(tanh_iz)
    return ComplexTensor(tanh_iz_im, -tanh_iz_re)

