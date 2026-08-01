
def _fft_c2c_aten(
    input: TensorLike,
    *,
    dim: DimsSequenceType,
    forward: bool,
) -> TensorLikeType:
    normalization = 0  # No normalization
    return torch._fft_c2c(input, dim, normalization, forward)

