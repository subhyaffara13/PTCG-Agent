
def infer_scale_swizzle(
    mat: torch.Tensor, scale: torch.Tensor
) -> tuple[Any | None, Any | None]:
    """
    Infer the scaling type and swizzle mode from matrix and scale tensor shapes/dtypes.

    This function determines how scale factors are laid out relative to the matrix:
    - TensorWise: Single scale for entire tensor
    - RowWise: One scale per row
    - BlockWise1x128/128x128: Block-scaled with float32 scales
    - BlockWise1x32: MXFP8 with float8_e8m0fnu scales (swizzled on NVIDIA)
    - BlockWise1x16: NVFP4 with float8_e4m3fn scales (swizzled)

    Args:
        mat: The matrix tensor (FP8 or FP4)
        scale: The scale factor tensor

    Returns:
        Tuple of (ScalingType, SwizzleType) or (None, None) if unrecognized
    """
    return _infer_scale_swizzle_impl(
        mat_size=(mat.shape[0], mat.shape[1]),
        scale_size=tuple(scale.shape),
        scale_numel=scale.numel(),
        mat_dtype=mat.dtype,
        scale_dtype=scale.dtype,
        eq_fn=lambda a, b: a == b,
    )

