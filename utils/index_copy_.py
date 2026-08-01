
def index_copy_(x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike):
    return _index_copy(x, dim, index, tensor, inplace=True)


def index_copy_(x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike):
    dim = utils.canonicalize_dims(x.ndim, dim)
    torch._check(
        index.ndim <= 1,
        lambda: f"Index should have dimension 1 or 0 (got {index.ndim})",
    )
    # Treat scalars as elements of \R^1
    y = x.unsqueeze(0) if x.ndim == 0 else x
    idx = (slice(None),) * dim + (index,)
    y[idx] = tensor
    return x

