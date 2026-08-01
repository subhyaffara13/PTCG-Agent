
def _reduce_multiple_axes(f, x, axis, keepdims=False, **kwargs):
    # Some reductions don't support multiple axes
    # (https://github.com/pytorch/pytorch/issues/56586).
    axes = _normalize_axes(axis, x.ndim)
    for a in reversed(axes):
        x = torch.movedim(x, a, -1)
    x = torch.flatten(x, -len(axes))

    out = f(x, -1, **kwargs)

    if keepdims:
        for a in axes:
            out = torch.unsqueeze(out, a)
    return out

