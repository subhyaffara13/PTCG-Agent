
def reduce_any(x, dim=None, keepdim=False):
    x = to_dtype(x, torch.bool)
    return make_reduction("any")(x, axis=dim, keepdims=keepdim)

