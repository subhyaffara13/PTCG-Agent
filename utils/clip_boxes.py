
def clip_boxes(box, box_size: tuple[int, int]):
    """
    Clip the boxes by limiting x coordinates to the range [0, width]
    and y coordinates to the range [0, height].

    Args:
        box (Tensor): The box to be clipped.
        box_size (height, width): The clipping box's size.
    """
    assert torch.isfinite(box).all(), "Box tensor contains infinite or NaN!"
    height, width = box_size
    x1 = box[:, 0].clamp(min=0, max=width)
    y1 = box[:, 1].clamp(min=0, max=height)
    x2 = box[:, 2].clamp(min=0, max=width)
    y2 = box[:, 3].clamp(min=0, max=height)
    box = torch.stack((x1, y1, x2, y2), dim=-1)

    return box

