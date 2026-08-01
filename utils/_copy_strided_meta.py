
def _copy_strided_meta(a: TensorLikeType, stride: ShapeType):
    if not isinstance(a, TensorLike):
        raise AssertionError(f"a must be TensorLike, got {type(a)}")  # mypy
    return torch.empty_strided(
        a.shape,
        stride,
        dtype=a.dtype,
        layout=a.layout,
        device=a.device,
        requires_grad=a.requires_grad,
    )

