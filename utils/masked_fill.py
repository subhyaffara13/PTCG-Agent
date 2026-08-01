
def masked_fill(a: TensorLikeType, mask: TensorLikeType, value: TensorOrNumberLikeType):
    python_type = utils.dtype_to_type(a.dtype)
    if isinstance(value, Number):
        value_type = type(value)
    else:
        # NOTE: Could not use value = item(value) as it resulted in
        # RuntimeError: Cannot cast FakeTensor(cpu) to number
        value_ndim = value.ndim
        torch._check(
            value_ndim == 0,
            lambda: f"only supports a 0-dimensional value tensor, but got tensor with {value_ndim} dimension",
        )
        # `masked_fill` allows cpu scalar to be moved to cuda, xpu and hpu but not otherwise.
        is_cpu_scalar = (
            a.device.type
            in ["cuda", "xpu", "mps", torch._C._get_privateuse1_backend_name(), "hpu"]
            and value.device.type == "cpu"
        )
        torch._check(
            is_cpu_scalar or value.device == a.device,
            lambda: "Expected `value` to be on same device as `a`",
        )
        value_type = utils.dtype_to_type(value.dtype)

    if value_type is complex:
        # only downcasting from complex to lower type is not allowed.
        # We allow casting `value` to lower type for other case
        # Eg. float -> int.
        # Ref: https://github.com/pytorch/pytorch/issues/79195
        torch._check(
            utils.is_weakly_lesser_type(value_type, python_type),
            lambda: f"could not convert to type {python_type} without overflow",
        )

    # Since `where` allows type-promotion,
    # cast value to correct type before passing to `where`

    value = _maybe_convert_to_dtype(value, a.dtype)
    r = torch.where(mask, value, a)  # type: ignore[arg-type]

    # aten.mask_fill always return a new contiguous tensor
    # contiguous() is needed to correctly model the output stride
    return r.contiguous()


def masked_fill(g: jit_utils.GraphContext, self, mask, value):
    """Implement the masked_fill functionality available for a pytorch tensor in ONNX.

    Fills elements of the input tensor with `value` where `mask` is True.
    """
    mask = g.op("Cast", mask, to_i=_C_onnx.TensorProtoDataType.BOOL)
    value = symbolic_helper._maybe_get_scalar(value)
    return g.op("Where", mask, symbolic_helper._if_scalar_type_as(value, self), self)

