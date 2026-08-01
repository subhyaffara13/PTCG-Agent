
def reverse_map_dim(dim_order, d):
    # Return the original PyTorch dimension position for a given dimension.
    # d should be the dimension that NNAPI will see.
    # reverse_map_dim(PRESUMED_CONTIGUOUS, x) == x
    # reverse_map_dim(CHANNELS_LAST, 3) == 1
    if dim_order in (DimOrder.PRESUMED_CONTIGUOUS, DimOrder.SCALAR_OR_VECTOR):
        return d
    if dim_order is DimOrder.CHANNELS_LAST:
        return [0, 2, 3, 1][d]
    raise AssertionError(f"expected DimOrder.CHANNELS_LAST, got {dim_order}")

