
def identity_trans(
    batch_dims: tuple[int, ...],
    dtype: torch.dtype | None = None,
    device: torch.device | None = None,
    requires_grad: bool = True,
) -> torch.Tensor:
    trans = torch.zeros((*batch_dims, 3), dtype=dtype, device=device, requires_grad=requires_grad)
    return trans

