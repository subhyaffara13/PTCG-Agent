
def _collapse_view_aten(a: Tensor, start: int, end: int) -> Tensor:
    new_shape = _collapsed_shape(a.shape, start, end)
    return a.view(new_shape)

