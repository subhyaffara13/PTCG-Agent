
def isclose_impl(
    self: ComplexTensor,
    rhs: ComplexTensor,
    rtol: float = 1e-5,
    atol: float = 1e-8,
    equal_nan: bool = False,
) -> torch.Tensor:
    abs_diff = torch.abs(self - rhs)
    abs_other = torch.abs(rhs)
    basic_condition = abs_diff <= (rtol * abs_other + atol)

    # This is the nontrivial part
    if equal_nan:
        a_r, a_i = split_complex_tensor(self)
        b_r, b_i = split_complex_arg(rhs)

        a_r_nan = torch.isnan(a_r)
        b_r_nan = torch.isnan(b_r)
        a_i_nan = torch.isnan(a_i)
        b_i_nan = torch.isnan(b_i)
        a_nan = a_r_nan | a_i_nan

        # This logical expression makes sure that the isnan of both the real and imaginary parts
        # matches (so 1 + nan*i doesn't equal nan + 1*i)
        equal_nan_condition = ((a_r_nan == b_r_nan) & (a_i_nan == b_i_nan)) & a_nan
        return basic_condition | equal_nan_condition

    return basic_condition

