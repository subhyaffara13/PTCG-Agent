
def meta_zeros(
    size,
    *,
    dtype=None,
    layout=None,
    device=None,
    pin_memory=None,
    requires_grad=False,
):
    if dtype is None:
        dtype = torch.get_default_dtype()
    if device is None:
        device = torch.get_default_device()
    if layout is None:
        layout = torch.strided
    return torch.empty(
        size, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )

