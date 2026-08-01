
def _calculate_shapes(broadcast_shape, dim_sizes, list_of_core_dims):
    """Helper for calculating broadcast shapes with core dimensions."""
    return [broadcast_shape + tuple(dim_sizes[dim] for dim in core_dims)
            for core_dims in list_of_core_dims]

