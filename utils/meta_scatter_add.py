
def meta_scatter_add(self, dim, index, src):
    scatter_meta_impl(self, dim, index, src, "add")
    return self.new_empty(self.shape)

