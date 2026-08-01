
def _broadcast_batch_norm_backward(x, broadcast_mask):
    for axis, mask in enumerate(broadcast_mask):
        if mask == 1 and not (axis < x.ndim and x.shape[axis] == mask):
            x = x.unsqueeze(axis)
    return x

