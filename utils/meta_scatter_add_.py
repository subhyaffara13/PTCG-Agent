
def meta_scatter_add_(self, dim, index, src):
    scatter_meta_impl(self, dim, index, src, "add")
    return self

