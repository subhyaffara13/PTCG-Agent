
def pow_impl(self: ComplexTensor, exponent: ComplexTensor) -> ComplexTensor:
    out_dt, (self, exponent) = promote_tensors(self, exponent)
    return torch.exp(exponent * torch.log(self)).to(out_dt)  # type: ignore[bad-return]

