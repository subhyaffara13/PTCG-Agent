
def empty_strided(
    size, stride, *, dtype=None, layout=None, device=None, pin_memory=None
):
    assert isinstance(size, (list, tuple))
    assert isinstance(stride, (list, tuple, type(None)))
    assert_nyi(layout in (None, torch.strided), f"layout={layout}")
    # pyrefly: ignore [bad-argument-type]
    dtype = decode_dtype(dtype) or torch.get_default_dtype()
    device = device or torch.tensor(0.0).device
    device = decode_device(device)
    pointwise = _full(fill_value=0, device=device, dtype=dtype, size=size)
    pointwise.realize()
    buffer = pointwise.data.data
    # explicitly set ranges to zeros in order to make a NopKernelSchedulerNode
    buffer.data = dataclasses.replace(buffer.data, ranges=[0] * len(size))
    assert isinstance(buffer, ir.ComputedBuffer)
    size = [sympy.expand(s) for s in size]
    stride = (
        [sympy.expand(s) for s in stride]
        if stride
        else ir.FlexibleLayout.contiguous_strides(size)
    )
    buffer.layout = ir.FixedLayout(
        device=device,
        dtype=dtype,
        size=size,
        stride=stride,
        is_pinned=pin_memory or False,
    )
    return pointwise


def empty_strided(
    shape: ShapeType | tuple[ShapeType],
    strides: StrideType,
    *,
    dtype: torch.dtype | None = None,
    device: DeviceLikeType | None = None,
    layout: torch.layout = torch.strided,
    requires_grad: bool = False,
    pin_memory: bool = False,
) -> TensorLikeType:
    # Layout == strided, pin_memory is False
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)

    shape = utils.extract_shape_from_varargs(shape)
    dtype = torch.get_default_dtype() if dtype is None else dtype
    device = torch.device("cpu") if device is None else device

    return prims.empty_strided(
        shape,
        strides,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,
    )

