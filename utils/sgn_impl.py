
def sgn_impl(self: ComplexTensor) -> ComplexTensor:
    self_r, self_i = split_complex_tensor(self)
    out_dt, (self_r, self_i) = promote_tensors(self_r, self_i)
    abs_self = torch.abs(ComplexTensor(self_r, self_i))
    mask = (self_r != 0) | (self_i != 0)
    masked_sgn = ComplexTensor(
        (self_r / abs_self).to(out_dt), (self_i / abs_self).to(out_dt)
    )
    return torch.where(mask, masked_sgn, 0)  # type: ignore[bad-return]

