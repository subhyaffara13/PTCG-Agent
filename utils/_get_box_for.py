
def _get_box_for(tensor: DTensor, idx: int) -> tuple[torch.Size, torch.Size]:
    offsets, size = _get_box(tensor)
    return (torch.Size([val * idx for val in offsets]), size)

