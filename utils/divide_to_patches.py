
def divide_to_patches(
    image: Union[np.ndarray, "torch.Tensor"], patch_size: int | tuple[int, int]
) -> list[Union[np.ndarray, "torch.Tensor"]]:
    """
    Divides an image into patches of a specified size.

    Args:
        image (`np.array | "torch.Tensor"`):
            The input image.
        patch_size (`int` or `tuple[int, int]`):
            The size of each patch. If an int, patches are square. If a tuple,
            it is interpreted as `(patch_height, patch_width)`.
    Returns:
        list: A list of `np.array | "torch.Tensor"` representing the patches.
    """
    patch_h, patch_w = (patch_size, patch_size) if isinstance(patch_size, int) else patch_size
    patches = []
    height, width = get_image_size(image, channel_dim=ChannelDimension.FIRST)
    for i in range(0, height, patch_h):
        for j in range(0, width, patch_w):
            patch = image[..., i : i + patch_h, j : j + patch_w]
            patches.append(patch)

    return patches

