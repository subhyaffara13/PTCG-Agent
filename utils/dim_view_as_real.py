
def dim_view_as_real(shape: Shape) -> DimMap:
    ndim = len(shape)
    results: list[DimSpec] = [InputDim(i) for i in range(ndim - 1)]
    # each complex number is split into two real numbers,
    # resulting in one more dimension of size 2
    results.append(Split(InputDim(ndim - 1), (shape[-1], 2), 0))
    results.append(Split(InputDim(ndim - 1), (shape[-1], 2), 1))
    return tuple(results)

