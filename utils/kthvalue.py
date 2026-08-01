
def kthvalue(self, k, dim=-1, keepdim=False):
    if not config.triton.decompose_sort_ops:
        return kthvalue_fallback(self, k, dim, keepdim)
    shape = self.get_size()
    ndim = len(shape)
    if ndim == 0:
        return clone(self), _full(0, self.get_device(), torch.int64, shape)
    dim = canonicalize_dim(ndim, dim)
    sorted_vals, sorted_idxs = sort_stable(self, stable=True, dim=dim)
    # k is 1-based
    values = select(sorted_vals, dim, k - 1)
    indices = select(sorted_idxs, dim, k - 1)
    if keepdim:
        values = unsqueeze(values, dim)
        indices = unsqueeze(indices, dim)
    return values, indices

