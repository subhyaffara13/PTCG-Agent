
def eq_impl(
    self: ComplexTensor, rhs: ComplexTensor, *args: Any, **kwargs: Any
) -> torch.Tensor:
    a_r, a_i = split_complex_arg(self)
    b_r, b_i = split_complex_arg(rhs)
    return torch.eq(a_r, b_r, *args, **kwargs) & torch.eq(a_i, b_i, *args, **kwargs)

