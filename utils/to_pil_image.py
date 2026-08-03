from typing import Union

def to_pil_image(
    image: Union[np.ndarray, "PIL.Image.Image", "torch.Tensor"],
    do_rescale: bool | None = None,
    image_mode: str | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> "PIL.Image.Image":
    """
    Converts `image` to a PIL Image. Optionally rescales it and puts the channel dimension back as the last axis if
    needed.

    Args:
        image (`PIL.Image.Image` or `numpy.ndarray` or `torch.Tensor`):
            The image to convert to the `PIL.Image` format.
        do_rescale (`bool`, *optional*):
            Whether or not to apply the scaling factor (to make pixel values integers between 0 and 255). Will default
            to `True` if the image type is a floating type and casting to `int` would result in a loss of precision,
            and `False` otherwise.
        image_mode (`str`, *optional*):
            The mode to use for the PIL image. If unset, will use the default mode for the input image type.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `PIL.Image.Image`: The converted image.
    """
    requires_backends(to_pil_image, ["vision"])

    if isinstance(image, PIL.Image.Image):
        return image

    # Convert all tensors to numpy arrays before converting to PIL image
    if is_torch_tensor(image):
        image = image.numpy()
    elif not isinstance(image, np.ndarray):
        raise ValueError(f"Input image type not supported: {type(image)}")

    # If the channel has been moved to first dim, we put it back at the end.
    image = to_channel_dimension_format(image, ChannelDimension.LAST, input_data_format)

    # If there is a single channel, we squeeze it, as otherwise PIL can't handle it.
    image = np.squeeze(image, axis=-1) if image.shape[-1] == 1 else image

    # PIL.Image can only store uint8 values so we rescale the image to be between 0 and 255 if needed.
    do_rescale = _rescale_for_pil_conversion(image) if do_rescale is None else do_rescale

    if do_rescale:
        image = rescale(image, 255)

    image = image.astype(np.uint8)
    return PIL.Image.fromarray(image, mode=image_mode)

