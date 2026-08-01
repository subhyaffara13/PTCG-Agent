
def fill_none_with_masks(data: list[torch.Tensor | None], masks: list[bool]):
    data_iter = iter(data)
    return [next(data_iter) if kept else None for kept in masks]

