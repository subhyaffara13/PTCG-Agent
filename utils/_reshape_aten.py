
def _reshape_aten(a: Tensor, shape: ShapeType) -> Tensor:
    return a.reshape(shape).clone(memory_format=torch.contiguous_format)

