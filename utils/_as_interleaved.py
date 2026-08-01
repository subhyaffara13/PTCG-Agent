
def _as_interleaved(arg: ComplexTensor | Any) -> Tensor | Any:
    """Convert a ComplexTensor to a Tensor with a complex dtype. Pass other arguments as-is."""
    if isinstance(arg, ComplexTensor):
        return arg.as_interleaved()
    return arg

