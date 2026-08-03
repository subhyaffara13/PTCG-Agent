import functools

def quantized_decomposed_quantize_per_tensor_default(
    input: TensorBox,
    scale: float,
    zero_point: int,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
) -> TensorBox:
    if input.get_dtype() == torch.bfloat16:
        input = to_dtype(input, torch.float32)
    assert input.get_dtype() == torch.float32, (
        f"Expecting input to have dtype torch.float32, but got dtype: {input.get_dtype()}"
    )

    input_loader = input.make_loader()

    def inner_fn(idx, scale, zero_point):
        input = input_loader(idx)
        inv_scale, zero_point = _create_constants(
            1.0 / scale, zero_point, dtype=torch.float32
        )
        val = ops.round(input * inv_scale) + zero_point
        qmin, qmax = _create_constants(quant_min, quant_max, dtype=torch.float32)
        clamped = ops.minimum(ops.maximum(val, qmin), qmax)
        return ops.to_dtype(clamped, dtype)

    return Pointwise.create(
        device=input.get_device(),
        dtype=dtype,
        inner_fn=functools.partial(
            inner_fn, scale=float(scale), zero_point=int(zero_point)
        ),
        ranges=input.get_size(),
    )

