
def _as_complex_tensor(arg: Tensor | Any) -> Tensor | ComplexTensor | Any:
    """Convert a Tensor with complex dtypes to a ComplexTensor. Pass along other args as-is."""
    if (
        not isinstance(arg, ComplexTensor)
        and isinstance(arg, Tensor)
        and arg.dtype in COMPLEX_TO_REAL
    ):
        return ComplexTensor.from_interleaved(arg)
    return arg

