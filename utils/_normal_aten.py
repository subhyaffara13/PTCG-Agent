
def _normal_aten(
    shape: ShapeType,
    *,
    mean: float | complex,
    std: float,
    dtype: torch.dtype,
    device: torch.device,
    requires_grad: bool,
    generator: torch.Generator | None = None,
) -> Tensor:
    a = torch.empty(shape, dtype=dtype, device=device, requires_grad=requires_grad)
    with torch.no_grad():
        # NOTE: normal_ is incorrectly annotated to expect mean to be a float
        a.normal_(mean, std, generator=generator)  # type: ignore[arg-type]
    return a

