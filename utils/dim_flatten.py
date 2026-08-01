
def dim_flatten(ndim: int, start_dim=0, end_dim=-1) -> DimMap:
    if ndim == 0:
        return (Singleton(),)
    elif ndim == 1:
        return (InputDim(0),)
    else:
        # only flattening dims from start_dim to end_dim (inclusive)
        # other dims are passed through
        if end_dim < 0:
            end_dim += ndim
        results: list[DimSpec] = [InputDim(i) for i in range(start_dim)]
        results.append(
            Flatten.new(tuple(InputDim(i) for i in range(start_dim, end_dim + 1)))
        )
        results.extend([InputDim(i) for i in range(end_dim + 1, ndim)])
        return tuple(results)

