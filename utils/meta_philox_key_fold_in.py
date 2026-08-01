
def meta_philox_key_fold_in(key, data):
    torch._check(
        key.dim() >= 1 and key.shape[-1] == 2,
        lambda: f"_philox_key_fold_in: key must have shape (*batch, 2), got shape {key.shape}",
    )
    torch._check(
        key.dtype == torch.uint64,
        lambda: f"_philox_key_fold_in: key must have dtype uint64, got {key.dtype}",
    )
    return torch.empty_like(key)

