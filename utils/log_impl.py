
def log_impl(self: ComplexTensor) -> ComplexTensor:
    out_dt, (self,) = promote_tensors(self)
    re = torch.log(torch.abs(self))
    im = torch.angle(self)
    return ComplexTensor(re, im).to(out_dt)  # type: ignore[bad-return]

