
def quantize_per_channel_group(
    input: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor,
    quant_min: int,
    quant_max: int,
    dtype: torch.dtype,
    group_size=128,
):
    if group_size <= 1:
        raise AssertionError("group_size must be > 1")
    # needed for GPTQ single column quantize
    if group_size > input.shape[-1] and scales.shape[-1] == 1:
        group_size = input.shape[-1]

    if input.shape[-1] % group_size != 0:
        raise AssertionError("input.shape[-1] must be divisible by group_size")
    if input.dim() != 2:
        raise AssertionError("input must be 2-dimensional")

    # TODO: check for dtype, currently we can't express torch.int4 so it's omitted
    to_quant = input.reshape(-1, group_size)
    if torch.isnan(to_quant).sum() != 0:
        raise AssertionError("to_quant must not contain NaNs")

    scales = scales.reshape(-1, 1)
    zero_points = zero_points.reshape(-1, 1)

    input_int8 = (
        to_quant.mul(1.0 / scales)
        .add(zero_points)
        .round()
        .clamp_(quant_min, quant_max)
        .to(dtype)
        .reshape_as(input)
    )

    return input_int8

