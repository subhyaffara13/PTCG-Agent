
def fake_quant_per_channel(
    input: torch.Tensor,
    scales: torch.Tensor,
    zero_points: torch.Tensor,
    axis: int,
    quant_min: int,
    quant_max: int,
) -> torch.Tensor:
    return FakeQuantPerChannel.apply(
        input, scales, zero_points, axis, quant_min, quant_max
    )

