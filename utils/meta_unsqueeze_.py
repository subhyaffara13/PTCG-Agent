
def meta_unsqueeze_(self, dim):
    dim = maybe_wrap_dim(dim, self.dim() + 1)
    g_sizes, g_strides = inferUnsqueezeGeometry(self, dim)
    self.as_strided_(g_sizes, g_strides)
    return self

