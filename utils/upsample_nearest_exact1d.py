
def upsample_nearest_exact1d(
    input: Tensor,
    output_size: list[int],
    scales: float | None = None,
) -> Tensor:
    return _upsample_nearest(input, output_size, [scales], exact=True)

