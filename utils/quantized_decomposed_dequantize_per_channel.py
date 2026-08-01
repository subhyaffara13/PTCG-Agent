
def quantized_decomposed_dequantize_per_channel(
    input: TensorBox,
    scales: TensorBox,
    zero_points: TensorBox,
    axis: int,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> TensorBox:
    assert len(scales.get_size()) == 1, "expect scales 1 dim"
    assert len(zero_points.get_size()) == 1, "expect zero_points 1 dim"
    assert input.get_dtype() == dtype, (
        f"Expecting input to have dtype {dtype}, but got dtype: {input.get_dtype()}"
    )
    assert axis < len(input.get_size()), (
        f"Expecting axis to be < {len(input.get_size())}"
    )

    if out_dtype is None:
        out_dtype = torch.float32

    input_loader = input.make_loader()
    scales_loader = scales.make_loader()
    zero_points_loader = zero_points.make_loader()

    def inner_fn(idx):
        channel_idx = (idx[axis],)

        input = input_loader(idx)
        scale = scales_loader(channel_idx)
        zero_point = zero_points_loader(channel_idx)

        if scales.dtype != torch.float32:
            scale = ops.to_dtype(scale, torch.float32)
        if zero_points.dtype != torch.float32:
            zero_point = ops.to_dtype(zero_point, torch.float32)
        val = ops.sub(ops.to_dtype(input, torch.float32), zero_point) * scale
        val = ops.to_dtype(val, out_dtype)
        return val

    return Pointwise.create(
        device=input.get_device(),
        dtype=out_dtype,
        inner_fn=inner_fn,
        ranges=input.get_size(),
    )

