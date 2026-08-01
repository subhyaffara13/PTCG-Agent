
def unpad_tensor(
    tensor: torch.Tensor, pad_dim: int, pad_size: IntLikeType
) -> torch.Tensor:
    # During tracing, always emit the narrow op even when pad_size=0 so all
    # ranks produce identical FX graph structure (SPMD).
    if guard_or_false(pad_size == 0) and not _are_we_tracing():
        return tensor
    return tensor.narrow(
        pad_dim,
        start=0,
        length=tensor.size(pad_dim) - pad_size,
    )

