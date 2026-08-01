
def exp_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)
    ex = torch.exp(x)
    u = ex * torch.cos(y)
    v = ex * torch.sin(y)
    return ComplexTensor(u.to(out_dt), v.to(out_dt))

