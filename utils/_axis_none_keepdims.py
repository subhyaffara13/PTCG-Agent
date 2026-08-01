
def _axis_none_keepdims(x, ndim, keepdims):
    # Apply keepdims when axis=None
    # (https://github.com/pytorch/pytorch/issues/71209)
    # Note that this is only valid for the axis=None case.
    if keepdims:
        for i in range(ndim):
            x = torch.unsqueeze(x, 0)
    return x

