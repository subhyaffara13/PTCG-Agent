
def quantized_decomposed_dequantize_per_tensor_default(
    input: TensorBox,
    scale: float,
    zero_point: int,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    *,
    out_dtype: torch.dtype | None = None,
) -> TensorBox:
    assert input.get_dtype() == dtype, (
        f"Expecting input to have dtype {dtype}, but got dtype: {input.get_dtype()}"
    )

    if out_dtype is None:
        out_dtype = torch.float32

    input_loader = input.make_loader()

    def inner_fn(idx, scale, zero_point):
        input = input_loader(idx)
        scale, zero_point = _create_constants(scale, zero_point, dtype=torch.float32)
        val = ops.sub(ops.to_dtype(input, torch.float32), zero_point) * scale
        val = ops.to_dtype(val, out_dtype)
        return val

    return Pointwise.create(
        device=input.get_device(),
        dtype=out_dtype,
        inner_fn=functools.partial(
            inner_fn, scale=float(scale), zero_point=int(zero_point)
        ),
        ranges=input.get_size(),
    )

