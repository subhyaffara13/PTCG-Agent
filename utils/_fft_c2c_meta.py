
def _fft_c2c_meta(
    input: TensorLike,
    *,
    dim: DimsSequenceType,
    forward: bool,
) -> TensorLikeType:
    dim = utils.canonicalize_dims(input.ndim, dim)
    utils.validate_no_repeating_dims(dim)

    shape = input.shape
    strides = utils.make_contiguous_strides_for(shape)
    return TensorMeta(
        shape=shape, strides=strides, dtype=input.dtype, device=input.device
    )

