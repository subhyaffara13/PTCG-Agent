
def upsample_nearest(  # noqa: F811
    input: Tensor,
    size: int | None = None,
    scale_factor: float | None = None,
    # pyrefly: ignore [bad-return]
) -> Tensor:
    pass


def upsample_nearest(  # noqa: F811
    input: Tensor,
    size: list[int] | None = None,
    scale_factor: float | None = None,
    # pyrefly: ignore [bad-return]
) -> Tensor:
    pass


def upsample_nearest(input, size=None, scale_factor=None):  # noqa: F811
    r"""Upsamples the input, using nearest neighbours' pixel values.

    .. warning::
        This function is deprecated in favor of :func:`torch.nn.functional.interpolate`.
        This is equivalent with ``nn.functional.interpolate(..., mode='nearest')``.

    Currently spatial and volumetric upsampling are supported (i.e. expected
    inputs are 4 or 5 dimensional).

    Args:
        input (Tensor): input
        size (int or Tuple[int, int] or Tuple[int, int, int]): output spatia
            size.
        scale_factor (int): multiplier for spatial size. Has to be an integer.

    Note:
        {backward_reproducibility_note}
    """
    # DeprecationWarning is ignored by default
    warnings.warn(
        "`nn.functional.upsample_nearest` is deprecated. "
        "Use `nn.functional.interpolate` instead.",
        stacklevel=2,
    )
    return interpolate(input, size, scale_factor, mode="nearest")


def upsample_nearest(input, size=None, scale_factor=None):
    r"""Upsamples the input, using nearest neighbours' pixel values.

    .. warning::
        This function is deprecated in favor of
        :func:`torch.ao.nn.quantized.functional.interpolate`.
        This is equivalent with ``nn.quantized.functional.interpolate(..., mode='nearest')``.

    .. note:: The input quantization parameters propagate to the output.

    .. note:: Only 2D inputs are supported

    Args:
        input (Tensor): quantized input
        size (int or Tuple[int, int] or Tuple[int, int, int]): output spatial
            size.
        scale_factor (int): multiplier for spatial size. Has to be an integer.
    """
    # DeprecationWarning is ignored by default
    warnings.warn(
        "nn.quantized.functional.upsample_nearest is deprecated. Use nn.quantized.functional.interpolate instead.",
        stacklevel=2,
    )
    return interpolate(input, size, scale_factor, mode="nearest")

