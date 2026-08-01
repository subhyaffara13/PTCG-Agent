
def _upsample_nearest_exact_vec(
    input: Tensor,
    output_size: list[int] | None,
    scale_factors: list[float] | None,
) -> Tensor:
    osize = upsample_compute_output_size(input.size(), output_size, scale_factors)
    scales = (
        scale_factors if scale_factors else [None] * len(osize)  # type: ignore[list-item]
    )
    return _upsample_nearest(input, osize, scales, exact=True)

