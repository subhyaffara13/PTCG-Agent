
def reorder_images(
    processed_images: dict[tuple[int, int], "torch.Tensor"],
    grouped_images_index: dict[int | tuple[int, int], tuple[tuple[int, int], int]],
    is_nested: bool = False,
) -> Union[list["torch.Tensor"], "torch.Tensor"]:
    """
    Reconstructs images in the original order, preserving the original structure (nested or not).
    The input structure is either all flat or all nested.

    Args:
        processed_images (dict[tuple[int, int], "torch.Tensor"]):
            Dictionary mapping shapes to batched processed images.
        grouped_images_index (dict[Union[int, tuple[int, int]], tuple[tuple[int, int], int]]):
            Dictionary mapping original indices to (shape, index) tuples.
        is_nested (bool, *optional*, defaults to False):
            Whether the images are nested. Cannot be inferred from the input, as some processing functions outputs nested images.
            even with non nested images,e.g functions splitting images into patches. We thus can't deduce is_nested from the input.


    Returns:
        Union[list["torch.Tensor"], "torch.Tensor"]:
            Images in the original structure.
    """
    if not is_nested:
        return [
            processed_images[grouped_images_index[i][0]][grouped_images_index[i][1]]
            for i in range(len(grouped_images_index))
        ]

    return _reconstruct_nested_structure(grouped_images_index, processed_images)

