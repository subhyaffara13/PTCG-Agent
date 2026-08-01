
def _describe_dim(njt, dim):
    if dim == 0:
        return "batch_dim"
    elif dim == njt._ragged_idx:
        return "ragged_dim"
    return "normal_dim"

