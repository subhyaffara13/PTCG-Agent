
def dim_squeeze(shape: Shape, dim: DimsType | None = None) -> DimMap:
    # Operates on local shape; sharding_prop rewrites squeeze ops to squeeze.dims
    # with only globally-singleton dims before this is called.
    from torch.fx.experimental.symbolic_shapes import guard_or_true

    ndim = len(shape)
    if dim is None:
        target_dims = set(range(ndim))
    elif isinstance(dim, int):
        target_dims = {normalize_dim(dim, ndim)}
    else:
        target_dims = set(normalize_dims(dim, ndim))
    return tuple(
        InputDim(i)
        for i, s in enumerate(shape)
        if guard_or_true(s > 1) or i not in target_dims
    )

