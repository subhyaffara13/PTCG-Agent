
def quantized_decomposed_dequantize_per_tensor_tensor(
    input: TensorBox,
    scale: TensorBox,
    zero_point: TensorBox,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> TensorBox:
    assert len(scale.get_size()) == 0 or (
        len(scale.get_size()) == 1 and scale.get_size()[0] == 1
    ), "expect scale as scalar tensor"
    assert len(zero_point.get_size()) == 0 or (
        len(zero_point.get_size()) == 1 and zero_point.get_size()[0] == 1
    ), "expect zero_point as scalar tensor"
    assert input.get_dtype() == dtype, (
        f"Expecting input to have dtype {dtype}, but got dtype: {input.get_dtype()}"
    )

    if out_dtype is None:
        out_dtype = torch.float32

    input_loader = input.make_loader()
    scale_loader = scale.make_loader()
    zero_point_loader = zero_point.make_loader()

    def inner_fn(idx):
        input = input_loader(idx)
        _scale = scale_loader((0,) if len(scale.get_size()) == 1 else ())
        _zero_point = zero_point_loader((0,) if len(scale.get_size()) == 1 else ())
        if scale.dtype != torch.float32:
            _scale = ops.to_dtype(_scale, torch.float32)
        if zero_point.dtype != torch.float32:
            _zero_point = ops.to_dtype(_zero_point, torch.float32)
        val = ops.sub(ops.to_dtype(input, torch.float32), _zero_point) * _scale
        val = ops.to_dtype(val, out_dtype)
        return val

    return Pointwise.create(
        device=input.get_device(),
        dtype=out_dtype,
        inner_fn=inner_fn,
        ranges=input.get_size(),
    )

