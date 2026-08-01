
def nonzero_static(self, *, size, fill_value: int = -1):
    # The impl of nonzero_static on xpu and mps differs from cuda but aligned with cpu
    if device_hint(self) in ("cpu", "mps", "xpu"):
        return self.new_empty((size, self.dim()), dtype=torch.long)
    else:
        return torch.empty_strided(
            (size, self.dim()),
            (1, size),
            dtype=torch.long,
            device=self.device,
        )

