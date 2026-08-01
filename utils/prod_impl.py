
def prod_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> ComplexTensor:
    out_dt, (self,) = promote_tensors(self)
    dtype = kwargs.pop("dtype", out_dt)
    kwargs["dtype"] = complex_to_real_dtype(self.dtype)

    prod_r = torch.prod(torch.abs(self), *args, **kwargs)
    sum_phi = torch.sum(torch.angle(self), *args, **kwargs)
    u = prod_r * torch.cos(sum_phi)
    v = prod_r * torch.sin(sum_phi)
    return ComplexTensor(u, v).to(dtype)  # type: ignore[bad-return]

