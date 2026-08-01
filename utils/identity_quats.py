
def identity_quats(
    batch_dims: tuple[int, ...],
    dtype: torch.dtype | None = None,
    device: torch.device | None = None,
    requires_grad: bool = True,
) -> torch.Tensor:
    quat = torch.zeros((*batch_dims, 4), dtype=dtype, device=device, requires_grad=requires_grad)

    with torch.no_grad():
        quat[..., 0] = 1

    return quat

