
def upsample_trilinear3d(
    input: Tensor,
    output_size: list[int],
    align_corners: bool,
    scales_d: float | None = None,
    scales_h: float | None = None,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_linear(
        input, output_size, align_corners, [scales_d, scales_h, scales_w]
    )

