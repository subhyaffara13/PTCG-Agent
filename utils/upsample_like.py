
def upsample_like(pixel_values: Tensor, like: Tensor, mode: str = "bilinear") -> Tensor:
    """
    An utility function that upsamples `pixel_values` to match the dimension of `like`.

    Args:
        pixel_values (`torch.Tensor`):
            The tensor we wish to upsample.
        like (`torch.Tensor`):
            The tensor we wish to use as size target.
        mode (str, *optional*, defaults to `"bilinear"`):
            The interpolation mode.

    Returns:
        `torch.Tensor`: The upsampled tensor
    """
    _, _, height, width = like.shape
    upsampled = nn.functional.interpolate(pixel_values, size=(height, width), mode=mode, align_corners=False)
    return upsampled

