
def get_image_size_fit_to_canvas(
    image_height: int,
    image_width: int,
    canvas_height: int,
    canvas_width: int,
    tile_size: int,
) -> tuple[int, int]:
    """
    Calculates the new size of an image to fit within a canvas while maintaining aspect ratio.

    This function calculates the optimal size for an image to fit within a canvas defined by
    canvas_height and canvas_width, while ensuring that the image dimensions are not smaller than
    tile_size. If the image is larger than the canvas, the returned size will fit within the canvas.
    If the image already fits within the canvas, the size remains unchanged.
    The aspect ratio of the original image is preserved as much as possible.

    Args:
        image_height (`int`):
            The height of the original image.
        image_width (`int`):
            The width of the original image.
        canvas_height (`int`):
            The height of the canvas.
        canvas_width (`int`):
            The width of the canvas.
        tile_size (`int`):
            The tile size.

    Returns:
        `tuple[int, int]`: A tuple containing the new height and width of the image.

    """
    # Set target image size in between `tile_size` and canvas_size
    target_width = np.clip(image_width, tile_size, canvas_width)
    target_height = np.clip(image_height, tile_size, canvas_height)

    scale_h = target_height / image_height
    scale_w = target_width / image_width

    if scale_w < scale_h:
        new_width = target_width
        # minimum height is 1 to avoid invalid height of 0
        new_height = min(math.floor(image_height * scale_w) or 1, target_height)
    else:
        new_height = target_height
        # minimum width is 1 to avoid invalid width of 0
        new_width = min(math.floor(image_width * scale_h) or 1, target_width)

    return new_height, new_width


def get_image_size_fit_to_canvas(
    image_height: int,
    image_width: int,
    canvas_height: int,
    canvas_width: int,
    tile_size: int,
) -> tuple[int, int]:
    """
    Calculates the new size of an image to fit within a canvas while maintaining aspect ratio.

    This function calculates the optimal size for an image to fit within a canvas defined by
    canvas_height and canvas_width, while ensuring that the image dimensions are not smaller than
    tile_size. If the image is larger than the canvas, the returned size will fit within the canvas.
    If the image already fits within the canvas, the size remains unchanged.
    The aspect ratio of the original image is preserved as much as possible.

    Args:
        image_height (`int`):
            The height of the original image.
        image_width (`int`):
            The width of the original image.
        canvas_height (`int`):
            The height of the canvas.
        canvas_width (`int`):
            The width of the canvas.
        tile_size (`int`):
            The tile size.

    Returns:
        `tuple[int, int]`: A tuple containing the new height and width of the image.

    """
    # Set target image size in between `tile_size` and canvas_size
    target_width = np.clip(image_width, tile_size, canvas_width)
    target_height = np.clip(image_height, tile_size, canvas_height)

    scale_h = target_height / image_height
    scale_w = target_width / image_width

    if scale_w < scale_h:
        new_width = target_width
        # minimum height is 1 to avoid invalid height of 0
        new_height = min(math.floor(image_height * scale_w) or 1, target_height)
    else:
        new_height = target_height
        # minimum width is 1 to avoid invalid width of 0
        new_width = min(math.floor(image_width * scale_h) or 1, target_width)

    return new_height, new_width

