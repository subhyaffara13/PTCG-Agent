
def scatter_add_(x, dim: int, index, src):
    return scatter_reduce_(x, dim, index, src, "sum")

