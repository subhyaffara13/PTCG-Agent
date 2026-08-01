
def pad_to_best_fit(
    images: "torch.Tensor",
    target_size: tuple[int, int],
    background_color: int | tuple[int, int, int] = 0,
) -> "torch.Tensor":
    """
    Pads an image to fit the target size.

    Args:
        images (`np.ndarray`):
            The images to pad.
        background_color (`int` or `tuple[int, int, int]`, *optional*, defaults to 0):
            The color to use for the padding. Can be an integer for single channel or a
            tuple of integers representing for multi-channel images. If passed as integer
            in multi-channel mode, it will default to `0` in subsequent channels.
    Returns:
        `torch.Tensor`: The padded images.
    """

    num_channels = images.shape[1] if len(images.shape) == 4 else images.shape[0]
    if isinstance(background_color, int):
        background_color = [background_color] + [0] * (num_channels - 1)
    elif len(background_color) != num_channels:
        raise ValueError(
            f"background_color must have no more than {num_channels} elements to match the number of channels"
        )

    height, width = images.shape[-2:]
    target_height, target_width = target_size
    paste_x_right = target_width - width
    paste_y_right = target_height - height
    padded_images = tvF.pad(images, padding=[0, 0, paste_x_right, paste_y_right], fill=background_color)

    return padded_images

