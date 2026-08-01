
def wrapped_quantized_linear(
    input: torch.Tensor,
    input_scale: torch.Tensor,
    input_zero_point: torch.Tensor,
    weight: torch.Tensor,
    weight_scale: torch.Tensor,
    weight_zero_point: torch.Tensor,
    bias: torch.Tensor,
    out_scale: torch.Tensor,
    out_zero_point: torch.Tensor,
    out_channel: int,
) -> torch.Tensor:
    packed_weight = torch.ops._quantized._wrapped_linear_prepack(
        weight, weight_scale, weight_zero_point, bias
    )
    return torch.ops._quantized._wrapped_quantized_linear_prepacked(
        input,
        input_scale,
        input_zero_point,
        packed_weight,
        out_scale,
        out_zero_point,
        out_channel,
    )

