
def find_closest_aspect_ratio(
    aspect_ratio: float,
    target_ratios: list[tuple[int, int]],
    width: int,
    height: int,
    image_size: int,
) -> tuple[int, int]:
    """Find the closest aspect ratio from target_ratios to match the input aspect ratio.

    Args:
        aspect_ratio: The aspect ratio to match (width/height).
        target_ratios: List of possible aspect ratios as tuples of (width, height) integers.
        width: Original image width in pixels.
        height: Original image height in pixels.
        image_size: Base size for calculating target area.

    Returns:
        tuple[int, int]: The best matching ratio as (width, height) integers.
    """
    best_ratio_diff = float("inf")
    best_ratio = (1, 1)
    area = width * height

    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)

        # update best ratio if we found a closer match
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        # if equally close, prefer the ratio that better matches the original image area
        elif ratio_diff == best_ratio_diff:
            target_area = image_size * image_size * ratio[0] * ratio[1]
            if area > 0.5 * target_area:
                best_ratio = ratio

    return best_ratio

