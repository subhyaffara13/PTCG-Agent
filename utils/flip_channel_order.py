
def flip_channel_order(
    image: np.ndarray,
    data_format: ChannelDimension | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> np.ndarray:
    """
    Flips the channel order of the image.

    If the image is in RGB format, it will be converted to BGR and vice versa.

    Args:
        image (`np.ndarray`):
            The image to flip.
        data_format (`ChannelDimension`, *optional*):
            The channel dimension format for the output image. Can be one of:
                - `ChannelDimension.FIRST`: image in (num_channels, height, width) format.
                - `ChannelDimension.LAST`: image in (height, width, num_channels) format.
            If unset, will use same as the input image.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format for the input image. Can be one of:
                - `ChannelDimension.FIRST`: image in (num_channels, height, width) format.
                - `ChannelDimension.LAST`: image in (height, width, num_channels) format.
            If unset, will use the inferred format of the input image.
    """
    input_data_format = infer_channel_dimension_format(image) if input_data_format is None else input_data_format

    if input_data_format == ChannelDimension.LAST:
        image = image[..., ::-1]
    elif input_data_format == ChannelDimension.FIRST:
        image = image[::-1, ...]
    else:
        raise ValueError(f"Unsupported channel dimension: {input_data_format}")

    if data_format is not None:
        image = to_channel_dimension_format(image, data_format, input_channel_dim=input_data_format)
    return image

