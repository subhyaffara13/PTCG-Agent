
def topk_meta(self, k, dim=-1, largest=True, sorted=True):
    # From aten/src/ATen/native/Sorting.cpp
    dim = maybe_wrap_dim(dim, self.dim(), wrap_scalar=True)
    sliceSize = 1 if self.dim() == 0 else self.size(dim)
    torch._check(k >= 0)
    torch._check(k <= sliceSize, lambda: "k not in range for dimension")

    topKSize = list(self.shape)
    if len(topKSize) > 0:
        topKSize[dim] = k
    return self.new_empty(topKSize), self.new_empty(topKSize, dtype=torch.int64)

