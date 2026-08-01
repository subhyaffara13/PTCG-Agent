
def _upsample_nearest_exact2d(
    input: Tensor,
    output_size: list[int],
    scales_h: float | None = None,
    scales_w: float | None = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales_h, scales_w], exact=True)


def _upsample_nearest_exact2d(
    x, output_size, scales_h: float | None = None, scales_w: float | None = None
):
    return upsample_nearestnd(x, output_size, (scales_h, scales_w), n=2, exact=True)

