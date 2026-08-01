
def reciprocal_impl(self: ComplexTensor) -> ComplexTensor:
    self_r, self_i = split_complex_tensor(self)
    out_dt, (self_r, self_i) = promote_tensors(self_r, self_i)
    den = self_r * self_r + self_i * self_i
    return ComplexTensor(
        aten.div(self_r, den).to(out_dt),
        aten.div(-self_i, den).to(out_dt),
    )

