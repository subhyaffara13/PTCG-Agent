
def _fft_c2r_aten(
    input: TensorLike,
    *,
    dim: DimsSequenceType,
    last_dim_size: int,
) -> TensorLikeType:
    normalization = 0  # No normalization
    return torch._fft_c2r(input, dim, normalization, last_dim_size)

