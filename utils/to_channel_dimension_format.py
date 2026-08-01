
def to_channel_dimension_format(
    image: np.ndarray,
    channel_dim: ChannelDimension | str,
    input_channel_dim: ChannelDimension | str | None = None,
) -> np.ndarray:
    """
    Converts `image` to the channel dimension format specified by `channel_dim`. The input
    can have arbitrary number of leading dimensions. Only last three dimension will be permuted
    to format the `image`.

    Args:
        image (`numpy.ndarray`):
            The image to have its channel dimension set.
        channel_dim (`ChannelDimension`):
            The channel dimension format to use.
        input_channel_dim (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If not provided, it will be inferred from the input image.

    Returns:
        `np.ndarray`: The image with the channel dimension set to `channel_dim`.
    """
    if not isinstance(image, np.ndarray):
        raise TypeError(f"Input image must be of type np.ndarray, got {type(image)}")

    if input_channel_dim is None:
        input_channel_dim = infer_channel_dimension_format(image)

    target_channel_dim = ChannelDimension(channel_dim)
    if input_channel_dim == target_channel_dim:
        return image

    if target_channel_dim == ChannelDimension.FIRST:
        axes = list(range(image.ndim - 3)) + [image.ndim - 1, image.ndim - 3, image.ndim - 2]
        image = image.transpose(axes)
    elif target_channel_dim == ChannelDimension.LAST:
        axes = list(range(image.ndim - 3)) + [image.ndim - 2, image.ndim - 1, image.ndim - 3]
        image = image.transpose(axes)
    else:
        raise ValueError(f"Unsupported channel dimension format: {channel_dim}")

    return image

