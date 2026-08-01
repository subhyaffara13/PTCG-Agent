
def upsample_linear1d(
    input: Tensor,
    output_size: list[int],
    align_corners: bool,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_linear(input, output_size, align_corners, [scales_w])

