
def safe_softmax(self, dim, dtype=None):
    out = torch.softmax(self, dim=dim, dtype=dtype)
    masked = self.eq(float("-inf"))
    masked_rows = torch.all(masked, dim=dim, keepdim=True)
    zeros = torch.zeros_like(out)
    return torch.where(masked_rows, zeros, out)

