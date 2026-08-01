
def _num_image_tokens(image_size: tuple[int, int], patch_size: tuple[int, int]) -> int:
    """
    Calculate the number of image tokens given the image size and patch size.

    Args:
        image_size (`tuple[int, int]`):
            The size of the image as `(height, width)`.
        patch_size (`tuple[int, int]`):
            The patch size as `(height, width)`.

    Returns:
        `int`: The number of image tokens.
    """
    height, width = image_size
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    num_width_tokens = (width - 1) // patch_width + 1
    num_height_tokens = (height - 1) // patch_height + 1
    return num_height_tokens, num_width_tokens


def _num_image_tokens(image_size: tuple[int, int], patch_size: tuple[int, int]) -> int:
    """
    Calculate the number of image tokens given the image size and patch size.

    Args:
        image_size (`tuple[int, int]`):
            The size of the image as `(height, width)`.
        patch_size (`tuple[int, int]`):
            The patch size as `(height, width)`.

    Returns:
        `int`: The number of image tokens.
    """
    height, width = image_size
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    num_width_tokens = (width - 1) // patch_width + 1
    num_height_tokens = (height - 1) // patch_height + 1
    return num_height_tokens, num_width_tokens


def _num_image_tokens(image_size: tuple[int, int], patch_size: tuple[int, int]) -> int:
    """
    Calculate the number of image tokens given the image size and patch size.

    Args:
        image_size (`tuple[int, int]`):
            The size of the image as `(height, width)`.
        patch_size (`tuple[int, int]`):
            The patch size as `(height, width)`.

    Returns:
        `int`: The number of image tokens.
    """
    height, width = image_size
    patch_height, patch_width = patch_size if isinstance(patch_size, (tuple, list)) else (patch_size, patch_size)
    num_width_tokens = (width - 1) // patch_width + 1
    num_height_tokens = (height - 1) // patch_height + 1
    return num_height_tokens, num_width_tokens

