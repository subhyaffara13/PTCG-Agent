
def new_empty_strided(
    x, size, stride, *, dtype=None, layout=None, device=None, pin_memory=None
):
    if dtype is None:
        dtype = x.get_dtype()
    if device is None:
        device = x.get_device()
    return empty_strided(
        size,
        stride,
        dtype=dtype,
        layout=layout,
        device=decode_device(device),
        pin_memory=pin_memory,
    )


def new_empty_strided(
    a: TensorLikeType,
    size: ShapeType,
    stride: StrideType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    """
    Reference implementation of torch.Tensor.new_empty_strided
    """

    dtype = a.dtype if dtype is None else dtype
    layout = a.layout if layout is None else layout
    device = a.device if device is None else device

    return torch.empty_strided(
        size,
        stride,
        dtype=dtype,
        device=device,
        pin_memory=pin_memory,
        layout=layout,
    )


def new_empty_strided(func, *args, **kwargs):
    _check_args_kwargs_length(args, kwargs, f"__torch_dispatch__, {func}", len_args=3)
    data = _get_data(args[0])
    mask = _maybe_get_mask(args[0])
    if tuple(args[1]) != tuple(data.size()):
        raise ValueError(
            f"__torch_dispatch__, {func}: args[1] expected to be the same as data.size()"
        )
    if tuple(args[2]) != tuple(data.stride()):
        raise ValueError(
            f"__torch_dispatch__, {func}: args[2] expected to be the same as data.stride()"
        )
    return MaskedTensor(func(data, args[1], args[2], **kwargs), mask)

