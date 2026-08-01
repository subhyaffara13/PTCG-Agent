
def scalar_tensor(s, dtype=None, layout=None, device=None, pin_memory=None):
    # NB: It's always wrong to try to create a scalar tensor with the jagged layout.
    # Rather than fix this everywhere, just use the strided layout and let NJT handle
    # scalar tensor broadcasting.
    if layout == torch.jagged:
        layout = torch.strided
    return torch.empty(
        (), dtype=dtype, layout=layout, device=device, pin_memory=pin_memory
    )


def scalar_tensor(
    a: NumberType,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType | None = None,
    pin_memory: bool = False,
) -> TensorLikeType:
    utils.check_layout(layout)
    utils.check_pin_memory(pin_memory)
    dtype = dtype if dtype is not None else utils.type_to_dtype(type(a))
    device = device if device is not None else torch.device("cpu")
    return prims.scalar_tensor(a, dtype=dtype, device=device)


def scalar_tensor(g: jit_utils.GraphContext, scalar, dtype, *options):
    dtype = symbolic_helper._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = _type_utils.JitScalarType.FLOAT
    scalar = g.op("Cast", scalar, to_i=_type_utils.JitScalarType(dtype).onnx_type())
    return scalar

