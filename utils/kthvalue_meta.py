
def kthvalue_meta(self, k, dim=-1, keepdim=False):
    from torch.fx.experimental.symbolic_shapes import sym_and

    dim = maybe_wrap_dim(dim, self.dim(), wrap_scalar=True)
    dimSize = self.size(dim) if self.dim() > 0 else 1
    torch._check(
        sym_and(k >= 1, k <= dimSize),
        lambda: f"kthvalue(): selected number k out of range for dimension {dim}",
    )

    shape = list(self.shape[:dim] + self.shape[dim + 1 :])
    if keepdim and self.dim() > 0:
        shape.insert(dim, 1)
    return self.new_empty(shape), self.new_empty(shape, dtype=torch.int64)

