
def _resize_aten(a: Tensor, shape: ShapeType) -> Tensor:
    return a.resize_(shape)

