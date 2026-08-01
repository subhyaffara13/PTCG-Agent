
def dim_unsqueeze(ndim: int, dim: int) -> DimMap:
    dims = tuple(InputDim(i) for i in range(ndim))
    if dim < 0:
        dim += ndim + 1
    return dims[:dim] + (Singleton(),) + dims[dim:]

