
def _empty_aten(
    shape: ShapeType, *, dtype: torch.dtype, device: torch.device, requires_grad: bool
) -> Tensor:
    return torch.empty(shape, dtype=dtype, device=device, requires_grad=requires_grad)

