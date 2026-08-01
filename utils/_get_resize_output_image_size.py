
def _get_resize_output_image_size(
    input_image: np.ndarray, output_size: tuple[int, int], keep_aspect_ratio: bool, multiple: int
) -> tuple[int, int]:
    """Get the output size for resizing an image."""
    input_height, input_width = get_image_size(input_image, channel_dim=ChannelDimension.FIRST)
    output_height, output_width = output_size

    # determine new height and width
    scale_height = output_height / input_height
    scale_width = output_width / input_width

    if keep_aspect_ratio:
        # scale as little as possible
        if abs(1 - scale_width) < abs(1 - scale_height):
            # fit width
            scale_height = scale_width
        else:
            # fit height
            scale_width = scale_height

    new_height = _constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = _constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return (new_height, new_width)


def _get_resize_output_image_size(
    input_image: "torch.Tensor",
    output_size: tuple[int, int],
    keep_aspect_ratio: bool,
    multiple: int,
) -> tuple[int, int]:
    """Get the output size for resizing an image."""
    input_height, input_width = input_image.shape[-2:]
    output_height, output_width = output_size

    # determine new height and width
    scale_height = output_height / input_height
    scale_width = output_width / input_width

    if keep_aspect_ratio:
        # scale as little as possible
        if abs(1 - scale_width) < abs(1 - scale_height):
            # fit width
            scale_height = scale_width
        else:
            # fit height
            scale_width = scale_height

    new_height = _constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = _constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return (new_height, new_width)

