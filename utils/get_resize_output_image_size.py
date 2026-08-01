
def get_resize_output_image_size(
    input_image: np.ndarray,
    size: int | tuple[int, int] | list[int] | tuple[int, ...],
    default_to_square: bool = True,
    max_size: int | None = None,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple:
    """
    Find the target (height, width) dimension of the output image after resizing given the input image and the desired
    size.

    Args:
        input_image (`np.ndarray`):
            The image to resize.
        size (`int` or `tuple[int, int]` or list[int] or `tuple[int]`):
            The size to use for resizing the image. If `size` is a sequence like (h, w), output size will be matched to
            this.

            If `size` is an int and `default_to_square` is `True`, then image will be resized to (size, size). If
            `size` is an int and `default_to_square` is `False`, then smaller edge of the image will be matched to this
            number. i.e, if height > width, then image will be rescaled to (size * height / width, size).
        default_to_square (`bool`, *optional*, defaults to `True`):
            How to convert `size` when it is a single int. If set to `True`, the `size` will be converted to a square
            (`size`,`size`). If set to `False`, will replicate
            [`torchvision.transforms.Resize`](https://pytorch.org/vision/stable/transforms.html#torchvision.transforms.Resize)
            with support for resizing only the smallest edge and providing an optional `max_size`.
        max_size (`int`, *optional*):
            The maximum allowed for the longer edge of the resized image: if the longer edge of the image is greater
            than `max_size` after being resized according to `size`, then the image is resized again so that the longer
            edge is equal to `max_size`. As a result, `size` might be overruled, i.e the smaller edge may be shorter
            than `size`. Only used if `default_to_square` is `False`.
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `tuple`: The target (height, width) dimension of the output image after resizing.
    """
    if isinstance(size, (tuple, list)):
        if len(size) == 2:
            return tuple(size)
        elif len(size) == 1:
            # Perform same logic as if size was an int
            size = size[0]
        else:
            raise ValueError("size must have 1 or 2 elements if it is a list or tuple")

    if default_to_square:
        return (size, size)

    height, width = get_image_size(input_image, input_data_format)
    short, long = (width, height) if width <= height else (height, width)
    requested_new_short = size

    new_short, new_long = requested_new_short, int(requested_new_short * long / short)

    if max_size is not None:
        if max_size <= requested_new_short:
            raise ValueError(
                f"max_size = {max_size} must be strictly greater than the requested "
                f"size for the smaller edge size = {size}"
            )
        if new_long > max_size:
            new_short, new_long = int(max_size * new_short / new_long), max_size

    return (new_long, new_short) if width <= height else (new_short, new_long)


def get_resize_output_image_size(
    input_image: Union[np.ndarray, "torch.Tensor"],
    shorter: int = 800,
    longer: int = 1333,
    size_divisor: int = 32,
) -> tuple[int, int]:
    """Get output image size after resizing with size_divisor."""
    if is_torch_available() and isinstance(input_image, torch.Tensor):
        input_height, input_width = input_image.shape[-2:]
    else:
        input_height, input_width = get_image_size(input_image, channel_dim=ChannelDimension.FIRST)

    min_size, max_size = shorter, longer
    scale = min_size / min(input_height, input_width)

    if input_height < input_width:
        new_height = min_size
        new_width = scale * input_width
    else:
        new_height = scale * input_height
        new_width = min_size

    if max(new_height, new_width) > max_size:
        scale = max_size / max(new_height, new_width)
        new_height = scale * new_height
        new_width = scale * new_width

    new_height, new_width = int(new_height + 0.5), int(new_width + 0.5)
    new_height = new_height // size_divisor * size_divisor
    new_width = new_width // size_divisor * size_divisor

    return new_height, new_width


def get_resize_output_image_size(
    input_image: np.ndarray,
    shorter: int = 800,
    longer: int = 1333,
    size_divisor: int = 32,
) -> tuple[int, int]:
    """Get output image size after resizing with size_divisor."""
    input_height, input_width = get_image_size(input_image, channel_dim=ChannelDimension.FIRST)

    min_size, max_size = shorter, longer
    scale = min_size / min(input_height, input_width)

    if input_height < input_width:
        new_height = min_size
        new_width = scale * input_width
    else:
        new_height = scale * input_height
        new_width = min_size

    if max(new_height, new_width) > max_size:
        scale = max_size / max(new_height, new_width)
        new_height = scale * new_height
        new_width = scale * new_width

    new_height, new_width = int(new_height + 0.5), int(new_width + 0.5)
    new_height = new_height // size_divisor * size_divisor
    new_width = new_width // size_divisor * size_divisor

    return new_height, new_width


def get_resize_output_image_size(
    input_image: "torch.Tensor",
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
) -> SizeDict:
    def constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
        x = round(val / multiple) * multiple

        if max_val is not None and x > max_val:
            x = math.floor(val / multiple) * multiple

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return SizeDict(height=new_height, width=new_width)


def get_resize_output_image_size(
    input_image: "torch.Tensor",
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
) -> SizeDict:
    def constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
        x = round(val / multiple) * multiple

        if max_val is not None and x > max_val:
            x = math.floor(val / multiple) * multiple

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return SizeDict(height=new_height, width=new_width)


def get_resize_output_image_size(
    input_image: np.ndarray,
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
) -> SizeDict:
    def constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
        x = round(val / multiple) * multiple

        if max_val is not None and x > max_val:
            x = math.floor(val / multiple) * multiple

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return SizeDict(height=new_height, width=new_width)


def get_resize_output_image_size(
    input_image: "torch.Tensor",
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
) -> SizeDict:
    def constrain_to_multiple_of(val, multiple, min_val=0, max_val=None):
        x = round(val / multiple) * multiple

        if max_val is not None and x > max_val:
            x = math.floor(val / multiple) * multiple

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return SizeDict(height=new_height, width=new_width)


def get_resize_output_image_size(image, size: SizeDict) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Images are always channels-first (CHW).
    """
    height, width = image.shape[-2:]

    min_len = size.shortest_edge
    max_len = size.longest_edge
    aspect_ratio = width / height

    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width


def get_resize_output_image_size(image, size: SizeDict) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Images are always channels-first (CHW).
    """
    height, width = image.shape[-2:]

    min_len = size.shortest_edge
    max_len = size.longest_edge
    aspect_ratio = width / height

    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width


def get_resize_output_image_size(
    image: "torch.Tensor",
    resolution_max_side: int,
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        image (`torch.Tensor`):
            Image to resize.
        resolution_max_side (`int`):
            The longest edge of the image will be resized to this value. The shortest edge will be resized to keep the
            input aspect ratio.
    Returns:
        The output size of the image after resizing.
    """
    height, width = image.shape[-2:]

    # Find the output size, when rescaling the longest edge to max_len and preserving the aspect ratio
    height, width = _resize_output_size_rescale_to_max_len(height, width, max_len=resolution_max_side)
    # Find the output size when scaling the image to be below the MAX_IMAGE_SIZE
    height, width = _resize_output_size_scale_below_upper_bound(height, width, max_len=MAX_IMAGE_SIZE)
    return height, width


def get_resize_output_image_size(
    image: np.ndarray,
    resolution_max_side: int,
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        image (`np.ndarray`):
            Image to resize.
        resolution_max_side (`int`):
            The longest edge of the image will be resized to this value. The shortest edge will be resized to keep the
            input aspect ratio.
    Returns:
        The output size of the image after resizing.
    """
    height, width = image.shape[-2:]

    # Find the output size, when rescaling the longest edge to max_len and preserving the aspect ratio
    height, width = _resize_output_size_rescale_to_max_len(height, width, max_len=resolution_max_side)
    # Find the output size when scaling the image to be below the MAX_IMAGE_SIZE
    height, width = _resize_output_size_scale_below_upper_bound(height, width, max_len=MAX_IMAGE_SIZE)
    return height, width


def get_resize_output_image_size(
    input_image: ImageInput,
    size: int | tuple[int, int] | list[int] | tuple[int],
    patch_size: int | tuple[int, int] | list[int] | tuple[int],
    input_data_format: str | ChannelDimension | None = None,
) -> tuple:
    """
    Find the target (height, width) dimension of the output image after resizing given the input image and the desired
    size.

    Args:
        input_image (`ImageInput`):
            The image to resize.
        size (`int` or `tuple[int, int]`):
            Max image size an input image can be. Must be a dictionary with the key "longest_edge".
        patch_size (`int` or `tuple[int, int]`):
            The patch_size as `(height, width)` to use for resizing the image. If patch_size is an integer, `(patch_size, patch_size)`
            will be used
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `tuple`: The target (height, width) dimension of the output image after resizing.
    """
    max_height, max_width = size if isinstance(size, (tuple, list)) else (size, size)
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    height, width = get_image_size(input_image, input_data_format)

    ratio = max(height / max_height, width / max_width)

    if ratio > 1:
        # Original implementation uses `round` which utilises bankers rounding, which can lead to surprising results
        # Here we use floor to ensure the image is always smaller than the given "longest_edge"
        height = int(math.floor(height / ratio))
        width = int(math.floor(width / ratio))

    num_height_tokens, num_width_tokens = _num_image_tokens((height, width), (patch_height, patch_width))
    return num_height_tokens * patch_height, num_width_tokens * patch_width


def get_resize_output_image_size(
    input_image: ImageInput,
    size: int | tuple[int, int] | list[int] | tuple[int],
    patch_size: int | tuple[int, int] | list[int] | tuple[int],
    input_data_format: str | ChannelDimension | None = None,
) -> tuple:
    """
    Find the target (height, width) dimension of the output image after resizing given the input image and the desired
    size.

    Args:
        input_image (`ImageInput`):
            The image to resize.
        size (`int` or `tuple[int, int]`):
            Max image size an input image can be. Must be a dictionary with the key "longest_edge".
        patch_size (`int` or `tuple[int, int]`):
            The patch_size as `(height, width)` to use for resizing the image. If patch_size is an integer, `(patch_size, patch_size)`
            will be used
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `tuple`: The target (height, width) dimension of the output image after resizing.
    """
    max_height, max_width = size if isinstance(size, (tuple, list)) else (size, size)
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    height, width = get_image_size(input_image, input_data_format)

    ratio = max(height / max_height, width / max_width)

    if ratio > 1:
        # Original implementation uses `round` which utilises bankers rounding, which can lead to surprising results
        # Here we use floor to ensure the image is always smaller than the given "longest_edge"
        height = int(math.floor(height / ratio))
        width = int(math.floor(width / ratio))

    num_height_tokens, num_width_tokens = _num_image_tokens((height, width), (patch_height, patch_width))
    return num_height_tokens * patch_height, num_width_tokens * patch_width


def get_resize_output_image_size(
    input_image: ImageInput,
    size: int | tuple[int, int] | list[int] | tuple[int],
    patch_size: int | tuple[int, int] | list[int] | tuple[int],
    input_data_format: str | ChannelDimension | None = None,
) -> tuple:
    """
    Find the target (height, width) dimension of the output image after resizing given the input image and the desired
    size.

    Args:
        input_image (`ImageInput`):
            The image to resize.
        size (`int` or `tuple[int, int]`):
            Max image size an input image can be. Must be a dictionary with the key "longest_edge".
        patch_size (`int` or `tuple[int, int]`):
            The patch_size as `(height, width)` to use for resizing the image. If patch_size is an integer, `(patch_size, patch_size)`
            will be used
        input_data_format (`ChannelDimension`, *optional*):
            The channel dimension format of the input image. If unset, will use the inferred format from the input.

    Returns:
        `tuple`: The target (height, width) dimension of the output image after resizing.
    """
    max_height, max_width = size if isinstance(size, (tuple, list)) else (size, size)
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    height, width = get_image_size(input_image, input_data_format)

    ratio = max(height / max_height, width / max_width)

    if ratio > 1:
        # Original implementation uses `round` which utilises bankers rounding, which can lead to surprising results
        # Here we use floor to ensure the image is always smaller than the given "longest_edge"
        height = int(math.floor(height / ratio))
        width = int(math.floor(width / ratio))

    num_height_tokens, num_width_tokens = _num_image_tokens((height, width), (patch_height, patch_width))
    return num_height_tokens * patch_height, num_width_tokens * patch_width


def get_resize_output_image_size(
    input_image: np.ndarray,
    longest_edge: int,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple[int, int]:
    height, width = get_image_size(input_image, input_data_format)
    if height >= width:
        ratio = width * 1.0 / height
        new_height = longest_edge
        new_width = int(new_height * ratio)
    else:
        ratio = height * 1.0 / width
        new_width = longest_edge
        new_height = int(new_width * ratio)
    return (new_height, new_width)


def get_resize_output_image_size(
    image: np.ndarray,
    resolution_max_side: int,
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        image (`np.ndarray`):
            Image to resize.
        resolution_max_side (`int`):
            The longest edge of the image will be resized to this value. The shortest edge will be resized to keep the
            input aspect ratio.
    Returns:
        The output size of the image after resizing.
    """
    height, width = image.shape[-2:]

    # Find the output size, when rescaling the longest edge to max_len and preserving the aspect ratio
    height, width = _resize_output_size_rescale_to_max_len(height, width, max_len=resolution_max_side)
    # Find the output size when scaling the image to be below the MAX_IMAGE_SIZE
    height, width = _resize_output_size_scale_below_upper_bound(height, width, max_len=MAX_IMAGE_SIZE)
    return height, width


def get_resize_output_image_size(
    image: "torch.Tensor",
    resolution_max_side: int,
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        image (`torch.Tensor`):
            Image to resize.
        resolution_max_side (`int`):
            The longest edge of the image will be resized to this value. The shortest edge will be resized to keep the
            input aspect ratio.
    Returns:
        The output size of the image after resizing.
    """
    height, width = image.shape[-2:]

    # Find the output size, when rescaling the longest edge to max_len and preserving the aspect ratio
    height, width = _resize_output_size_rescale_to_max_len(height, width, max_len=resolution_max_side)
    # Find the output size when scaling the image to be below the MAX_IMAGE_SIZE
    height, width = _resize_output_size_scale_below_upper_bound(height, width, max_len=MAX_IMAGE_SIZE)
    return height, width


def get_resize_output_image_size(
    video,
    resolution_max_side: int,
) -> tuple[int, int]:
    """
    Get the output size of the video after resizing given a dictionary specifying the max and min sizes.
    Args:
        video (`np.ndarray`):
            Video to resize.
        resolution_max_side (`int`):
            The longest edge of the video will be resized to this value. The shortest edge will be resized to keep the
            input aspect ratio.
    Returns:
        The output size of the video after resizing.
    """
    height, width = video.size()[-2:]

    # Find the output size, when rescaling the longest edge to max_len and preserving the aspect ratio
    # The output size must be below the MAX_IMAGE_SIZE
    resolution_max_side = min(MAX_IMAGE_SIZE, resolution_max_side)
    resolution_max_side = max(height, width) if resolution_max_side is None else resolution_max_side
    aspect_ratio = width / height

    if width >= height:
        width = resolution_max_side
        height = int(width / aspect_ratio)
        if height % 2 != 0:
            height += 1
    elif height > width:
        height = resolution_max_side
        width = int(height * aspect_ratio)
        if width % 2 != 0:
            width += 1

    height = max(height, 1)
    width = max(width, 1)

    return height, width


def get_resize_output_image_size(
    input_image: np.ndarray,
    max_size: int = 448,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple[int, int]:
    height, width = get_image_size(input_image, input_data_format)
    if height >= width:
        ratio = width * 1.0 / height
        new_height = max_size
        new_width = new_height * ratio
    else:
        ratio = height * 1.0 / width
        new_width = max_size
        new_height = new_width * ratio
    size = (int(new_height), int(new_width))

    return size


def get_resize_output_image_size(
    input_image: np.ndarray,
    shorter: int = 800,
    longer: int = 1333,
    size_divisor: int = 32,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple[int, int]:
    input_height, input_width = get_image_size(input_image, input_data_format)
    min_size, max_size = shorter, longer

    scale = min_size / min(input_height, input_width)

    if input_height < input_width:
        new_height = min_size
        new_width = scale * input_width
    else:
        new_height = scale * input_height
        new_width = min_size

    if max(new_height, new_width) > max_size:
        scale = max_size / max(new_height, new_width)
        new_height = scale * new_height
        new_width = scale * new_width

    new_height, new_width = int(new_height + 0.5), int(new_width + 0.5)
    new_height = new_height // size_divisor * size_divisor
    new_width = new_width // size_divisor * size_divisor

    return new_height, new_width


def get_resize_output_image_size(
    input_image: "torch.Tensor | np.ndarray",
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple[int, int]:
    def constrain_to_multiple_of(val, multiple, min_val=0):
        x = (np.round(val / multiple) * multiple).astype(int)

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

    output_size = (output_size, output_size) if isinstance(output_size, int) else output_size

    input_height, input_width = get_image_size(input_image, input_data_format)
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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return (new_height, new_width)


def get_resize_output_image_size(
    input_image: "torch.Tensor | np.ndarray",
    output_size: int | Iterable[int],
    keep_aspect_ratio: bool,
    multiple: int,
    input_data_format: str | ChannelDimension | None = None,
) -> tuple[int, int]:
    def constrain_to_multiple_of(val, multiple, min_val=0):
        x = (np.round(val / multiple) * multiple).astype(int)

        if x < min_val:
            x = math.ceil(val / multiple) * multiple

        return x

    output_size = (output_size, output_size) if isinstance(output_size, int) else output_size

    input_height, input_width = get_image_size(input_image, input_data_format)
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

    new_height = constrain_to_multiple_of(scale_height * input_height, multiple=multiple)
    new_width = constrain_to_multiple_of(scale_width * input_width, multiple=multiple)

    return (new_height, new_width)

