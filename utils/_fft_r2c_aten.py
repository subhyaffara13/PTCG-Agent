
def _fft_r2c_aten(
    input: TensorLike,
    *,
    dim: DimsSequenceType,
    onesided: bool,
) -> TensorLikeType:
    normalization = 0  # No normalization
    return torch._fft_r2c(input, dim, normalization, onesided)

