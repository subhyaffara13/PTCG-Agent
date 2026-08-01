
def mask_border(tensor: torch.Tensor, border_margin: int, value: bool | float | int) -> torch.Tensor:
    """
    Mask a tensor border with a given value

    Args:
        tensor (`torch.Tensor` of shape `(batch_size, height_0, width_0, height_1, width_1)`):
            The tensor to mask
        border_margin (`int`) :
            The size of the border
        value (`Union[bool, int, float]`):
            The value to place in the tensor's borders

    Returns:
        tensor (`torch.Tensor` of shape `(batch_size, height_0, width_0, height_1, width_1)`):
            The masked tensor
    """
    if border_margin <= 0:
        return tensor

    tensor[:, :border_margin] = value
    tensor[:, :, :border_margin] = value
    tensor[:, :, :, :border_margin] = value
    tensor[:, :, :, :, :border_margin] = value
    tensor[:, -border_margin:] = value
    tensor[:, :, -border_margin:] = value
    tensor[:, :, :, -border_margin:] = value
    tensor[:, :, :, :, -border_margin:] = value

    return tensor

