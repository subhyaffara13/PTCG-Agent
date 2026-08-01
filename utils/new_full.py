
def new_full(
    a: TensorLikeType,
    size: ShapeType,
    fill_value: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.full(
        size,
        fill_value,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
    )


def new_full(
    g: jit_utils.GraphContext,
    self,
    size,
    fill_value,
    dtype,
    layout,
    device,
    pin_memory=False,
):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    if symbolic_helper._is_none(dtype) and self_dtype is not None:
        dtype = self_dtype
    return full(g, size, fill_value, dtype, layout, device, pin_memory)

