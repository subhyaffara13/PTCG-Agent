
def get_aspect_ratio_preserving_size(
    height: int,
    width: int,
    patch_size: int,
    max_patches: int,
    pooling_kernel_size: int,
) -> tuple[int, int]:
    """
    Image is resized to preserve aspect ratio so it fits within the patch budget.
    Target dimensions are the largest that:
    1) Produce at most `max_patches` patches when patchified with `patch_size`
    2) Have height and width divisible by `pooling_kernel_size * patch_size`
    """
    total_px = height * width
    target_px = max_patches * (patch_size**2)
    factor = math.sqrt(target_px / total_px)
    ideal_height = factor * height
    ideal_width = factor * width
    side_mult = pooling_kernel_size * patch_size

    # Round down to nearest multiple of side_mult
    target_height = int(math.floor(ideal_height / side_mult)) * side_mult
    target_width = int(math.floor(ideal_width / side_mult)) * side_mult

    # Handle edge cases where one or both dimensions round to 0
    if target_height == 0 and target_width == 0:
        raise ValueError(
            "Attempting to resize to a 0 x 0 image. Resized height should be divisble by "
            f"`pooling_kernel_size * patch_size`={pooling_kernel_size * patch_size}."
        )

    max_side_length = (max_patches // pooling_kernel_size**2) * side_mult
    if target_height == 0:
        target_height = side_mult
        target_width = min(
            int(math.floor(width / height)) * side_mult,
            max_side_length,
        )
    elif target_width == 0:
        target_width = side_mult
        target_height = min(
            int(math.floor(height / width)) * side_mult,
            max_side_length,
        )

    if target_height * target_width > target_px:
        raise ValueError(
            f"Resizing [{height}x{width}] to [{target_height}x{target_width}] "
            f"but this exceeds {max_patches} patches with patch_size {patch_size}"
        )

    return target_height, target_width


def get_aspect_ratio_preserving_size(
    height: int,
    width: int,
    patch_size: int,
    max_patches: int,
    pooling_kernel_size: int,
) -> tuple[int, int]:
    """
    Image is resized to preserve aspect ratio so it fits within the patch budget.
    Target dimensions are the largest that:
    1) Produce at most `max_patches` patches when patchified with `patch_size`
    2) Have height and width divisible by `pooling_kernel_size * patch_size`
    """
    total_px = height * width
    target_px = max_patches * (patch_size**2)
    factor = math.sqrt(target_px / total_px)
    ideal_height = factor * height
    ideal_width = factor * width
    side_mult = pooling_kernel_size * patch_size

    # Round down to nearest multiple of side_mult
    target_height = int(math.floor(ideal_height / side_mult)) * side_mult
    target_width = int(math.floor(ideal_width / side_mult)) * side_mult

    # Handle edge cases where one or both dimensions round to 0
    if target_height == 0 and target_width == 0:
        raise ValueError(
            "Attempting to resize to a 0 x 0 image. Resized height should be divisble by "
            f"`pooling_kernel_size * patch_size`={pooling_kernel_size * patch_size}."
        )

    max_side_length = (max_patches // pooling_kernel_size**2) * side_mult
    if target_height == 0:
        target_height = side_mult
        target_width = min(
            int(math.floor(width / height)) * side_mult,
            max_side_length,
        )
    elif target_width == 0:
        target_width = side_mult
        target_height = min(
            int(math.floor(height / width)) * side_mult,
            max_side_length,
        )

    if target_height * target_width > target_px:
        raise ValueError(
            f"Resizing [{height}x{width}] to [{target_height}x{target_width}] "
            f"but this exceeds {max_patches} patches with patch_size {patch_size}"
        )

    return target_height, target_width


def get_aspect_ratio_preserving_size(
    height: int,
    width: int,
    patch_size: int,
    max_patches: int,
    pooling_kernel_size: int,
) -> tuple[int, int]:
    """
    Image is resized to preserve aspect ratio so it fits within the patch budget.
    Target dimensions are the largest that:
    1) Produce at most `max_patches` patches when patchified with `patch_size`
    2) Have height and width divisible by `pooling_kernel_size * patch_size`
    """
    total_px = height * width
    target_px = max_patches * (patch_size**2)
    factor = math.sqrt(target_px / total_px)
    ideal_height = factor * height
    ideal_width = factor * width
    side_mult = pooling_kernel_size * patch_size

    # Round down to nearest multiple of side_mult
    target_height = int(math.floor(ideal_height / side_mult)) * side_mult
    target_width = int(math.floor(ideal_width / side_mult)) * side_mult

    # Handle edge cases where one or both dimensions round to 0
    if target_height == 0 and target_width == 0:
        raise ValueError(
            "Attempting to resize to a 0 x 0 image. Resized height should be divisble by "
            f"`pooling_kernel_size * patch_size`={pooling_kernel_size * patch_size}."
        )

    max_side_length = (max_patches // pooling_kernel_size**2) * side_mult
    if target_height == 0:
        target_height = side_mult
        target_width = min(
            int(math.floor(width / height)) * side_mult,
            max_side_length,
        )
    elif target_width == 0:
        target_width = side_mult
        target_height = min(
            int(math.floor(height / width)) * side_mult,
            max_side_length,
        )

    if target_height * target_width > target_px:
        raise ValueError(
            f"Resizing [{height}x{width}] to [{target_height}x{target_width}] "
            f"but this exceeds {max_patches} patches with patch_size {patch_size}"
        )

    return target_height, target_width


def get_aspect_ratio_preserving_size(
    height: int,
    width: int,
    patch_size: int,
    max_patches: int,
    pooling_kernel_size: int,
) -> tuple[int, int]:
    """
    Image is resized to preserve aspect ratio so it fits within the patch budget.
    Target dimensions are the largest that:
    1) Produce at most `max_patches` patches when patchified with `patch_size`
    2) Have height and width divisible by `pooling_kernel_size * patch_size`
    """
    total_px = height * width
    target_px = max_patches * (patch_size**2)
    factor = math.sqrt(target_px / total_px)
    ideal_height = factor * height
    ideal_width = factor * width
    side_mult = pooling_kernel_size * patch_size

    # Round down to nearest multiple of side_mult
    target_height = int(math.floor(ideal_height / side_mult)) * side_mult
    target_width = int(math.floor(ideal_width / side_mult)) * side_mult

    # Handle edge cases where one or both dimensions round to 0
    if target_height == 0 and target_width == 0:
        raise ValueError(
            "Attempting to resize to a 0 x 0 image. Resized height should be divisble by "
            f"`pooling_kernel_size * patch_size`={pooling_kernel_size * patch_size}."
        )

    max_side_length = (max_patches // pooling_kernel_size**2) * side_mult
    if target_height == 0:
        target_height = side_mult
        target_width = min(
            int(math.floor(width / height)) * side_mult,
            max_side_length,
        )
    elif target_width == 0:
        target_width = side_mult
        target_height = min(
            int(math.floor(height / width)) * side_mult,
            max_side_length,
        )

    if target_height * target_width > target_px:
        raise ValueError(
            f"Resizing [{height}x{width}] to [{target_height}x{target_width}] "
            f"but this exceeds {max_patches} patches with patch_size {patch_size}"
        )

    return target_height, target_width


def get_aspect_ratio_preserving_size(
    height: int,
    width: int,
    patch_size: int,
    max_patches: int,
    pooling_kernel_size: int,
) -> tuple[int, int]:
    """
    Image is resized to preserve aspect ratio so it fits within the patch budget.
    Target dimensions are the largest that:
    1) Produce at most `max_patches` patches when patchified with `patch_size`
    2) Have height and width divisible by `pooling_kernel_size * patch_size`
    """
    total_px = height * width
    target_px = max_patches * (patch_size**2)
    factor = math.sqrt(target_px / total_px)
    ideal_height = factor * height
    ideal_width = factor * width
    side_mult = pooling_kernel_size * patch_size

    # Round down to nearest multiple of side_mult
    target_height = int(math.floor(ideal_height / side_mult)) * side_mult
    target_width = int(math.floor(ideal_width / side_mult)) * side_mult

    # Handle edge cases where one or both dimensions round to 0
    if target_height == 0 and target_width == 0:
        raise ValueError(
            "Attempting to resize to a 0 x 0 image. Resized height should be divisble by "
            f"`pooling_kernel_size * patch_size`={pooling_kernel_size * patch_size}."
        )

    max_side_length = (max_patches // pooling_kernel_size**2) * side_mult
    if target_height == 0:
        target_height = side_mult
        target_width = min(
            int(math.floor(width / height)) * side_mult,
            max_side_length,
        )
    elif target_width == 0:
        target_width = side_mult
        target_height = min(
            int(math.floor(height / width)) * side_mult,
            max_side_length,
        )

    if target_height * target_width > target_px:
        raise ValueError(
            f"Resizing [{height}x{width}] to [{target_height}x{target_width}] "
            f"but this exceeds {max_patches} patches with patch_size {patch_size}"
        )

    return target_height, target_width

