
def _collapse_aten(a: Tensor, start: int, end: int) -> Tensor:
    new_shape = _collapsed_shape(a.shape, start, end)
    out = a.new_empty(new_shape)
    with torch.no_grad():
        out.view_as(a).copy_(a)
    return out

