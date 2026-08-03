from typing import Any

def cumprod_impl(self: ComplexTensor, *args: Any, **kwargs: Any) -> ComplexTensor:
    dtype = kwargs.pop("dtype", self.dtype)
    kwargs["dtype"] = complex_to_real_dtype(dtype)

    prod_r = torch.cumprod(torch.abs(self), *args, **kwargs)
    sum_phi = torch.cumsum(torch.angle(self), *args, **kwargs)
    u = prod_r * torch.cos(sum_phi)
    v = prod_r * torch.sin(sum_phi)
    return ComplexTensor(u, v)

