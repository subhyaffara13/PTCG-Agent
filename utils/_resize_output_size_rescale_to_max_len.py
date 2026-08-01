
def _resize_output_size_rescale_to_max_len(
    height: int, width: int, min_len: int | None = 1, max_len: int | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        min_len (`int`, *optional*, defaults to 1):
            Minimum size of the output image.
        max_len (`int`, *optional*, defaults to the maximum size of the image):
            Maximum size of the output image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len
    aspect_ratio = width / height

    if width >= height:
        width = max_len
        height = int(width / aspect_ratio)
        if height % 2 != 0:
            height += 1
    elif height > width:
        height = max_len
        width = int(height * aspect_ratio)
        if width % 2 != 0:
            width += 1

    # Avoid resizing to a size smaller than min_len
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width


def _resize_output_size_rescale_to_max_len(
    height: int, width: int, min_len: int | None = 1, max_len: int | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        min_len (`int`, *optional*, defaults to 1):
            Minimum size of the output image.
        max_len (`int`, *optional*, defaults to the maximum size of the image):
            Maximum size of the output image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len
    aspect_ratio = width / height

    if width >= height:
        width = max_len
        height = int(width / aspect_ratio)
        if height % 2 != 0:
            height += 1
    elif height > width:
        height = max_len
        width = int(height * aspect_ratio)
        if width % 2 != 0:
            width += 1

    # Avoid resizing to a size smaller than min_len
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width


def _resize_output_size_rescale_to_max_len(
    height: int, width: int, min_len: int | None = 1, max_len: int | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        min_len (`int`, *optional*, defaults to 1):
            Minimum size of the output image.
        max_len (`int`, *optional*, defaults to the maximum size of the image):
            Maximum size of the output image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len
    aspect_ratio = width / height

    if width >= height:
        width = max_len
        height = int(width / aspect_ratio)
        if height % 2 != 0:
            height += 1
    elif height > width:
        height = max_len
        width = int(height * aspect_ratio)
        if width % 2 != 0:
            width += 1

    # Avoid resizing to a size smaller than min_len
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width


def _resize_output_size_rescale_to_max_len(
    height: int, width: int, min_len: int | None = 1, max_len: int | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        min_len (`int`, *optional*, defaults to 1):
            Minimum size of the output image.
        max_len (`int`, *optional*, defaults to the maximum size of the image):
            Maximum size of the output image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len
    aspect_ratio = width / height

    if width >= height:
        width = max_len
        height = int(width / aspect_ratio)
        if height % 2 != 0:
            height += 1
    elif height > width:
        height = max_len
        width = int(height * aspect_ratio)
        if width % 2 != 0:
            width += 1

    # Avoid resizing to a size smaller than min_len
    height = max(height, min_len)
    width = max(width, min_len)
    return height, width

