
def reference_unbind(t, dim):
    """A numpy implementation of torch.unbind"""
    return tuple(s.squeeze(dim) for s in np.split(t, t.shape[dim], dim))

