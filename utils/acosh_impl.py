
def acosh_impl(self: ComplexTensor) -> ComplexTensor:
    out_dt, (self,) = promote_tensors(self)
    return torch.log(self + torch.sqrt(self * self - 1)).to(out_dt)  # type: ignore[bad-return]

