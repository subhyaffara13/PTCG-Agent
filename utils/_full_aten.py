
def _full_aten(
    shape: ShapeType,
    fill_value: NumberType,
    *,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
) -> Tensor:
    # Note that Mypy thinks torch.full can't accept a complex fill_value
    return torch.full(
        shape,
        fill_value,
        dtype=dtype,
        device=device,
        requires_grad=requires_grad,  # type: ignore[arg-type]
    )

