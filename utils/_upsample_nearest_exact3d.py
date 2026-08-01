
def _upsample_nearest_exact3d(
    input: Tensor,
    output_size: list[int],
    scales_d: float | None = None,
    scales_h: float | None = None,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_nearest(
        input, output_size, [scales_d, scales_h, scales_w], exact=True
    )


def _upsample_nearest_exact3d(
    x,
    output_size,
    scales_d: float | None = None,
    scales_h: float | None = None,
    scales_w: float | None = None,
):
    return upsample_nearestnd(
        x, output_size, (scales_d, scales_h, scales_w), n=3, exact=True
    )

