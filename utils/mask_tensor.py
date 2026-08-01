
def mask_tensor(mask: TensorLikeType, t: TensorLikeType):
    """
    Similar to torch.where(mask, t, 0) but if t is boolean,
    result is also boolean and not promoted to int.
    """
    # torch.where(mask, t, False) is equivalent
    # but feels hacky and might break in the future
    if t.dtype is torch.bool:
        return mask.logical_and(t)
    else:
        return torch.where(mask, t, 0)

