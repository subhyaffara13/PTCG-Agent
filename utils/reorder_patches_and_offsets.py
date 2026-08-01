
def reorder_patches_and_offsets(
    patches: list[torch.Tensor], offsets: list[list[int]]
) -> tuple[list[torch.Tensor], list[list[int]]]:
    """Sorts patches and offsets according to the original image index."""

    combined = list(zip(offsets, patches))
    combined.sort(key=lambda x: x[0][0])
    sorted_offsets, sorted_patches = zip(*combined)

    return list(sorted_patches), list(sorted_offsets)

