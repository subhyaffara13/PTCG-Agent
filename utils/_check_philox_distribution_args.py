
def _check_philox_distribution_args(op_name, self, key):
    torch._check(
        self.dtype.is_floating_point,
        lambda: f"{op_name}: self must be a floating point tensor, got {self.dtype}",
    )
    torch._check(
        key.dtype == torch.uint64,
        lambda: f"{op_name}: key must have dtype uint64, got {key.dtype}",
    )
    torch._check(
        self.device == key.device,
        lambda: (
            f"{op_name}: self and key must be on the same device, "
            f"got {self.device} and {key.device}"
        ),
    )
    torch._check(
        key.dim() >= 1 and key.shape[-1] == 2,
        lambda: (
            f"{op_name}: key must have shape (2,) or (*batch, 2), got shape {key.shape}"
        ),
    )
    if key.dim() > 1:
        torch._check(
            key.dim() == self.dim() + 1,
            lambda: (
                f"{op_name}: batched key must have ndim == output ndim + 1, "
                f"got key shape {key.shape} with output shape {self.shape}"
            ),
        )
        key_batch = key.shape[: self.dim()]
        torch._check(
            all(ks == 1 or ks == ss for ks, ss in zip(key_batch, self.shape)),
            lambda: (
                f"{op_name}: key batch shape {list(key_batch)} "
                f"is not broadcastable with output shape {self.shape}"
            ),
        )

