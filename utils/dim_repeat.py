
def dim_repeat(ndim: int, sizes: Shape) -> DimMap:
    sizes = normalize_sizes(sizes)
    if not len(sizes) >= ndim:
        raise AssertionError(
            f"Number of dimensions of repeat dims {sizes} can not be smaller than number of dimensions of tensor {ndim}."
        )
    pad = len(sizes) - ndim
    return tuple(Repeat.new(Singleton(), s) for s in sizes[:pad]) + tuple(
        Repeat.new(InputDim(i), s) for i, s in enumerate(sizes[pad:])
    )

