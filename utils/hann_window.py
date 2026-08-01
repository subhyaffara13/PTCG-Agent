
def hann_window(
    window_length: int,
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: torch.device | None = None,
    pin_memory: bool | None = None,
) -> Tensor:
    """hann_window(window_length, *, dtype=None, layout=None, device=None, pin_memory=False) -> Tensor

    Returns a Hann window of size :attr:`window_length` with ``periodic=True``.

    Equivalent to :func:`torch.hann_window` with ``periodic=True``.

    Args:
        window_length (int): the size of returned window.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): desired dtype. Default: global default.
        layout (:class:`torch.layout`, optional): desired layout. Default: ``torch.strided``.
        device (:class:`torch.device`, optional): desired device. Default: current device.
        pin_memory (bool, optional): if ``True``, pins the returned tensor. Default: ``False``.
    """
    return aten.hann_window.periodic(
        window_length,
        True,
        dtype=dtype,
        layout=layout,
        device=device,
        pin_memory=pin_memory,
    )


def hann_window(
    g: jit_utils.GraphContext,
    window_length,
    periodic=True,
    dtype: int | None = None,
    layout=None,
    device=None,
    pin_memory=None,
    requires_grad=False,
):
    if dtype is None:
        dtype_ = torch.get_default_dtype()
        if not dtype_ or not dtype_.is_floating_point:
            dtype_ = torch.float
        scalar_type = _type_utils.JitScalarType.from_dtype(dtype_)
    else:
        scalar_type = _type_utils.JitScalarType(dtype)

    n_array = arange(g, window_length, 4, None, None, None)
    output = g.op("Cast", n_array, to_i=_C_onnx.TensorProtoDataType.FLOAT)
    output = mul(
        g, g.op("Constant", value_t=torch.tensor(math.pi, dtype=torch.float)), output
    )

    if periodic is False:
        window_length = sub(
            g, window_length, g.op("Constant", value_t=torch.tensor(1, dtype=torch.int))
        )
    output = div(g, output, window_length)
    output = g.op(
        "Cast",
        square(g, sin(g, output)),
        to_i=scalar_type.onnx_type(),
    )

    return output

