
def tracked_empty_strided(
    size: list[int],
    stride: list[int],
    *,
    dtype: torch.dtype,
    device: torch.device,
    name: str,
) -> torch.Tensor:
    o = torch.empty_strided(size, stride, dtype=dtype, device=device)
    track_tensor(o, name)
    return o

