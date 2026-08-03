import math


def get_max_res_without_distortion(
    image_size: tuple[int, int],
    target_size: tuple[int, int],
) -> tuple[int, int]:
    """
    Determines the maximum resolution to which an image can be resized to without distorting its
    aspect ratio, based on the target resolution.

    Args:
        image_size (tuple[int, int]): The original resolution of the image (height, width).
        target_resolution (tuple[int, int]): The desired resolution to fit the image into (height, width).
    Returns:
        tuple[int, int]: The optimal dimensions (height, width) to which the image should be resized.
    Example:
        >>> _get_max_res_without_distortion([200, 300], target_size = [450, 200])
        (134, 200)
        >>> _get_max_res_without_distortion([800, 600], target_size = [450, 1300])
        (450, 338)
    """

    original_height, original_width = image_size
    target_height, target_width = target_size

    scale_w = target_width / original_width
    scale_h = target_height / original_height

    if scale_w < scale_h:
        new_width = target_width
        new_height = min(math.floor(original_height * scale_w), target_height)
    else:
        new_height = target_height
        new_width = min(math.floor(original_width * scale_h), target_width)

    return new_height, new_width

