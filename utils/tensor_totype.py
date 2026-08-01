
def tensor_totype(t):
    dtype = (
        torch.float
        if (
            t.is_mps
            or (t.is_xpu and not torch.xpu.get_device_properties(t.device).has_fp64)
            or t.is_maia
        )
        else torch.double
    )
    return t.to(dtype=dtype)

