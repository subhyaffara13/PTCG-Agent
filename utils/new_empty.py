
def new_empty(x, size, *, dtype=None, layout=None, device=None, pin_memory=None):
    if dtype is None:
        dtype = x.get_dtype()
    if device is None:
        device = x.get_device()
    return empty_strided(
        size,
        None,
        dtype=dtype,
        layout=layout,
        device=decode_device(device),
        pin_memory=pin_memory,
    )


def new_empty(
    a: TensorLikeType,
    size: ShapeType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.empty(
        size,
        dtype=dtype,
        device=device,
        pin_memory=pin_memory,
        layout=layout,
    )


def new_empty(
    g: jit_utils.GraphContext, self, sizes, dtype, layout, device, pin_memory=False
):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    if symbolic_helper._is_none(dtype) and self_dtype is not None:
        dtype = self_dtype
    return empty(g, sizes, dtype, layout, device, pin_memory)

