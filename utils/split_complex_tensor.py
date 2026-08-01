
def split_complex_tensor(complex_tensor: ComplexTensor) -> tuple[Tensor, Tensor]:
    """Split a ComplexTensor into its real and imaginary parts."""
    return complex_tensor.re, complex_tensor.im

