
def median_dim(self, dim, keepdim=False):
    if not config.triton.decompose_sort_ops:
        return median_dim_fallback(self, dim, keepdim)
    shape = self.get_size()
    ndim = len(shape)
    if ndim == 0:
        return clone(self), _full(0, self.get_device(), torch.int64, shape)
    dim = canonicalize_dim(ndim, dim)
    sorted_vals, sorted_idxs = sort_stable(self, stable=True, dim=dim)
    n = shape[dim]
    k = (n - 1) // 2
    values = select(sorted_vals, dim, k)
    indices = select(sorted_idxs, dim, k)
    if keepdim:
        values = unsqueeze(values, dim)
        indices = unsqueeze(indices, dim)
    return values, indices

