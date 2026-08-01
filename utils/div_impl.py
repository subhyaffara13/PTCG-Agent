
def div_impl(
    lhs: ComplexTensor, rhs: ComplexTensor, *, rounding_mode: str | None = None
) -> ComplexTensor:
    if rounding_mode is not None:
        raise NotImplementedError(
            "`rounding_mode` other than `None` not implemented for`ComplexTensor`."
        )
    a_r, a_i = split_complex_arg(lhs)
    if not is_complex(rhs):
        return ComplexTensor(a_r / rhs, a_i / rhs)
    b_r, b_i = split_complex_arg(rhs)
    out_dt, (a_r, a_i, b_r, b_i) = promote_tensors(a_r, a_i, b_r, b_i)
    num_r = a_r * b_r + a_i * b_i
    num_i = a_i * b_r - a_r * b_i
    den = b_r * b_r + b_i * b_i
    return ComplexTensor(
        (num_r / den).to(out_dt),
        (num_i / den).to(out_dt),
    )

