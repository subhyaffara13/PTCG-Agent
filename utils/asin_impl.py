
def asin_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    asinh_iz = torch.asinh(ComplexTensor(-y, x))
    if not isinstance(asinh_iz, ComplexTensor):
        raise AssertionError(f"asinh_iz must be a ComplexTensor, got {type(asinh_iz)}")
    asinh_iz_re, asinh_iz_im = split_complex_tensor(asinh_iz)
    return ComplexTensor(asinh_iz_im, -asinh_iz_re)

