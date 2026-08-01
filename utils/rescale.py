
def rescale(
    image: np.ndarray,
    scale: float,
    data_format: ChannelDimension | None = None,
    dtype: np.dtype = np.float32,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Rescales `image` by `scale`.

    Args:
        image (`np.ndarray`):
            The image to rescale.
        scale (`float`):
            The scale to use for rescaling the image.
        data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the image. If not provided, it will be the same as the input image.
        dtype (`np.dtype`, *optional*, defaults to `np.float32`):
            The dtype of the output image. Defaults to `np.float32`. Used for backwards compatibility with feature
            extractors.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If not provided, it will be inferred from the input image.

    Returns:
        `np.ndarray`: The rescaled image.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Input image must be of type np.ndarray, got {type(image)}")

    rescaled_image = image.astype(np.float64) * scale  # Numpy type promotion has changed, so always upcast first
    if data_format is not None:
        rescaled_image = to_channel_dimension_format(rescaled_image, data_format, input_data_format)

    rescaled_image = rescaled_image.astype(dtype)  # Finally downcast to the desired dtype at the end

    return rescaled_image


def rescale(y, W, H, mi, ma):
    """Rescale the given array `y` to fit into the integer values
    between `0` and `H-1` for the values between ``mi`` and ``ma``.
    """
    y_new = []

    norm = ma - mi
    offset = (ma + mi) / 2

    for x in range(W):
        if is_valid(y[x]):
            normalized = (y[x] - offset) / norm
            if not is_valid(normalized):
                y_new.append(None)
            else:
                rescaled = Float((normalized*H + H/2) * (H-1)/H).round()
                rescaled = int(rescaled)
                y_new.append(rescaled)
        else:
            y_new.append(None)
    return y_new

