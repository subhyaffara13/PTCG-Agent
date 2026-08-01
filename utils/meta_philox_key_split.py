
def meta_philox_key_split(key, num_splits):
    torch._check(
        key.dim() >= 1 and key.shape[-1] == 2,
        lambda: f"_philox_key_split: key must have shape (*batch, 2), got shape {key.shape}",
    )
    torch._check(
        key.dtype == torch.uint64,
        lambda: f"_philox_key_split: key must have dtype uint64, got {key.dtype}",
    )
    torch._check(
        num_splits > 0,
        lambda: f"_philox_key_split: num_splits must be positive, got {num_splits}",
    )
    batch_sizes = key.shape[:-1]
    return key.new_empty((num_splits, *batch_sizes, 2))

