
def filter_with_masks(data: list[torch.Tensor | None], masks: list[bool]):
    if len(data) != len(masks):
        raise AssertionError(
            f"data length ({len(data)}) != masks length ({len(masks)})"
        )
    return [item for item, keep in zip(data, masks) if keep]

