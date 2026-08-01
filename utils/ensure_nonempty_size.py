
def ensure_nonempty_size(t, dim):
    return 1 if t.dim() == 0 else t.shape[dim]

