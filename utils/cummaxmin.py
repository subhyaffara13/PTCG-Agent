
def cummaxmin(self, dim):
    values = torch.empty(self.shape, device=self.device, dtype=self.dtype)
    indices = torch.empty(self.shape, device=self.device, dtype=torch.int64)
    if self.numel() != 0 and self.ndim != 0:
        # Checks that dim is within bounds
        maybe_wrap_dim(dim, self.ndim)
    return values, indices

