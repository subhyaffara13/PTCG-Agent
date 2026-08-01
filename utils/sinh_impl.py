
def sinh_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)
    u = torch.sinh(x) * torch.cos(y)
    v = torch.cosh(x) * torch.sin(y)
    return ComplexTensor(u.to(out_dt), v.to(out_dt))

