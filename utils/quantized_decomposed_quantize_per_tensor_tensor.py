
def quantized_decomposed_quantize_per_tensor_tensor(
    input: TensorBox,
    scale: TensorBox,
    zero_point: TensorBox,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
) -> TensorBox:
    if input.get_dtype() == torch.bfloat16:
        input = to_dtype(input, torch.float32)
    assert input.get_dtype() == torch.float32, (
        f"Expecting input to have dtype torch.float32, but got dtype: {input.get_dtype()}"
    )
    assert len(scale.get_size()) == 0 or (
        len(scale.get_size()) == 1 and scale.get_size()[0] == 1
    ), "expect scale as scalar tensor"
    assert len(zero_point.get_size()) == 0 or (
        len(zero_point.get_size()) == 1 and zero_point.get_size()[0] == 1
    ), "expect zero_point as scalar tensor"

    input_loader = input.make_loader()
    scale_loader = scale.make_loader()
    zero_point_loader = zero_point.make_loader()

    device = input.get_device()

    def inner_fn(idx):
        input = input_loader(idx)
        _scale = scale_loader((0,) if len(scale.get_size()) == 1 else ())
        _zero_point = zero_point_loader((0,) if len(scale.get_size()) == 1 else ())
        if scale.dtype != torch.float32:
            _scale = ops.to_dtype(_scale, torch.float32)
        if zero_point.dtype != torch.float32:
            _zero_point = ops.to_dtype(_zero_point, torch.float32)
        if device and device.type == "cpu":
            val = ops.fma(input, ops.reciprocal(_scale), _zero_point)
            return ops.round_to_int(val, dtype)
        val = ops.round(input * ops.reciprocal(_scale)) + _zero_point
        qmin, qmax = _create_constants(quant_min, quant_max, dtype=torch.float32)
        clamped = ops.minimum(ops.maximum(val, qmin), qmax)
        return ops.to_dtype(clamped, dtype)

    return Pointwise.create(
        device=input.get_device(),
        dtype=dtype,
        inner_fn=inner_fn,
        ranges=input.get_size(),
    )

