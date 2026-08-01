
def dim_pad_left(ndim: int, min_dims: int) -> DimMap:
    return (Singleton(),) * max(0, min_dims - ndim) + tuple(
        InputDim(i) for i in range(ndim)
    )

