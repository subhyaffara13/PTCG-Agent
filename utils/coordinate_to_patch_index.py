import math


def coordinate_to_patch_index(bbox: tuple[float, float, float, float], num_patches_per_side: int) -> tuple[int, int]:
    """Convert a bounding box to a pair of patch indices.

    Args:
        bbox (`tuple[float, float, float, float]`):
            The 4 coordinates of the bounding box, with the format being (x1, y1, x2, y2) specifying the upper-left and
            lower-right corners of the box. It should have x2 > x1 and y2 > y1.
        num_patches_per_side (`int`): the number of patches along each side.

    Returns:
        `tuple[int, int]`: A pair of patch indices representing the upper-left patch and lower-right patch.
    """
    (x1, y1, x2, y2) = bbox

    if not (x2 > x1 and y2 > y1):
        raise ValueError("The coordinates in `bbox` should be `(x1, y1, x2, y2)` with `x2 > x1` and `y2 > y1`.")

    ul_x = math.floor(x1 * num_patches_per_side)
    ul_y = math.floor(y1 * num_patches_per_side)

    lr_x = math.ceil(x2 * num_patches_per_side - 1)
    lr_y = math.ceil(y2 * num_patches_per_side - 1)

    ul_idx = ul_y * num_patches_per_side + ul_x
    lr_idx = lr_y * num_patches_per_side + lr_x

    return ul_idx, lr_idx

