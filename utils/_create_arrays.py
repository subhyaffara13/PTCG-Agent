
def _create_arrays(broadcast_shape, dim_sizes, list_of_core_dims, dtypes,
                   results=None):
    """Helper for creating output arrays in vectorize."""
    shapes = _calculate_shapes(broadcast_shape, dim_sizes, list_of_core_dims)
    if dtypes is None:
        dtypes = [None] * len(shapes)
    if results is None:
        arrays = tuple(np.empty(shape=shape, dtype=dtype)
                       for shape, dtype in zip(shapes, dtypes))
    else:
        arrays = tuple(np.empty_like(result, shape=shape, dtype=dtype)
                       for result, shape, dtype
                       in zip(results, shapes, dtypes))
    return arrays

