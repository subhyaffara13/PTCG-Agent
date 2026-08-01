
def _copy_strided_aten(a: Tensor, stride: ShapeType) -> Tensor:
    out = torch.empty_strided(
        a.size(),
        stride=stride,
        dtype=a.dtype,
        layout=a.layout,
        device=a.device,
        requires_grad=a.requires_grad,
    )
    out.copy_(a)
    return out

