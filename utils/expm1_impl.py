
def expm1_impl(self: ComplexTensor) -> ComplexTensor:
    x, y = split_complex_tensor(self)
    out_dt, (x, y) = promote_tensors(x, y)
    # TODO (hameerabbasi): The two lines below may have numerical issues
    ex = torch.exp(x)
    u = ex * torch.cos(y) - 1
    v = ex * torch.sin(y)
    return ComplexTensor(u.to(out_dt), v.to(out_dt))

