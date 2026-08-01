
def _index_copy(
    x: TensorLike, dim: int, index: TensorLike, tensor: TensorLike, *, inplace: bool
):
    dim = utils.canonicalize_dims(x.ndim, dim)
    torch._check(
        index.ndim <= 1,
        lambda: f"Index should have dimension 1 or 0 (got {index.ndim})",
    )
    # Treat scalars as elements of \R^1
    zero_dim = x.ndim == 0
    x1 = x.unsqueeze(0) if zero_dim else x
    index = index.unsqueeze(0) if index.ndim == 0 else index
    idx = (None,) * dim + (index,)
    index_put = aten.index_put_ if inplace else aten.index_put
    out = index_put(x1, idx, tensor)
    if inplace:
        return x
    else:
        return out.squeeze(0) if zero_dim else out.contiguous()

