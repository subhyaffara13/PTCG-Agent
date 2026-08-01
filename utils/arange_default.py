
def arange_default(
    end: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: torch.device | None = None,
    pin_memory: bool = False,
):
    return aten.arange.start_step(
        0, end, 1, dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )

