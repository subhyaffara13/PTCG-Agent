
def resize_image_high_res(
    width: int,
    height: int,
) -> Tuple[int, int]:
    # Maximum dimensions for high res mode
    max_short_side = MAX_SHORT_SIDE_FOR_IMAGE_HIGH_RES
    max_long_side = MAX_LONG_SIDE_FOR_IMAGE_HIGH_RES

    # Return early if no resizing is needed
    if (
        width <= MAX_SHORT_SIDE_FOR_IMAGE_HIGH_RES
        and height <= MAX_SHORT_SIDE_FOR_IMAGE_HIGH_RES
    ):
        return width, height

    # Determine the longer and shorter sides
    longer_side = max(width, height)
    shorter_side = min(width, height)

    # Calculate the aspect ratio
    aspect_ratio = longer_side / shorter_side

    # Resize based on the short side being 768px
    if width <= height:  # Portrait or square
        resized_width = max_short_side
        resized_height = int(resized_width * aspect_ratio)
        # if the long side exceeds the limit after resizing, adjust both sides accordingly
        if resized_height > max_long_side:
            resized_height = max_long_side
            resized_width = int(resized_height / aspect_ratio)
    else:  # Landscape
        resized_height = max_short_side
        resized_width = int(resized_height * aspect_ratio)
        # if the long side exceeds the limit after resizing, adjust both sides accordingly
        if resized_width > max_long_side:
            resized_width = max_long_side
            resized_height = int(resized_width / aspect_ratio)

    return resized_width, resized_height

