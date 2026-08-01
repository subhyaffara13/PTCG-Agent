
def _resize_output_size_scale_below_upper_bound(
    height: int, width: int, max_len: dict[str, int] | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        max_len (`Dict[str, int]`, *optional*, defaults to the maximum size of the image):
            Defines the maximum dimensions of the image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len

    aspect_ratio = width / height
    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)

    # Avoid resizing to a size smaller than 1
    height = max(height, 1)
    width = max(width, 1)
    return height, width


def _resize_output_size_scale_below_upper_bound(
    height: int, width: int, max_len: dict[str, int] | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        max_len (`Dict[str, int]`, *optional*, defaults to the maximum size of the image):
            Defines the maximum dimensions of the image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len

    aspect_ratio = width / height
    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)

    # Avoid resizing to a size smaller than 1
    height = max(height, 1)
    width = max(width, 1)
    return height, width


def _resize_output_size_scale_below_upper_bound(
    height: int, width: int, max_len: dict[str, int] | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        max_len (`Dict[str, int]`, *optional*, defaults to the maximum size of the image):
            Defines the maximum dimensions of the image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len

    aspect_ratio = width / height
    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)

    # Avoid resizing to a size smaller than 1
    height = max(height, 1)
    width = max(width, 1)
    return height, width


def _resize_output_size_scale_below_upper_bound(
    height: int, width: int, max_len: dict[str, int] | None = None
) -> tuple[int, int]:
    """
    Get the output size of the image after resizing given a dictionary specifying the max and min sizes.
    Args:
        height (`int`):
            Height of the input image.
        width (`int`):
            Width of the input image.
        max_len (`Dict[str, int]`, *optional*, defaults to the maximum size of the image):
            Defines the maximum dimensions of the image.
    Returns:
        The output size of the image after resizing.
    """
    max_len = max(height, width) if max_len is None else max_len

    aspect_ratio = width / height
    if width >= height and width > max_len:
        width = max_len
        height = int(width / aspect_ratio)
    elif height > width and height > max_len:
        height = max_len
        width = int(height * aspect_ratio)

    # Avoid resizing to a size smaller than 1
    height = max(height, 1)
    width = max(width, 1)
    return height, width

