
def meta_scatter_(self, dim, index, src_or_value, reduce=None):
    src = src_or_value if isinstance(src_or_value, torch.Tensor) else None
    scatter_meta_impl(self, dim, index, src, reduce)
    return self

