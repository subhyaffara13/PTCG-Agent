
def _get_quat(quat_key: str, dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    return torch.tensor(_CACHED_QUATS[quat_key], dtype=dtype, device=device)

