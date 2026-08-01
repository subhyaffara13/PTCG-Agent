
def _outer_to_inner_dim(ndim, dim, ragged_dim, canonicalize=False):
    from torch._prims_common import canonicalize_dims

    if isinstance(dim, (tuple, list)):
        output = type(dim)(_outer_to_inner_dim(ndim, d, ragged_dim) for d in dim)
        # ensure no duplicates, which can result from both batch and ragged mapping to 0
        return type(output)(dict.fromkeys(output))

    if canonicalize:
        dim = canonicalize_dims(ndim, dim)

    if not (dim >= 0 and dim < ndim):  # pyrefly: ignore [unsupported-operation]
        raise AssertionError(f"dim {dim} out of range for ndim {ndim}")

    # Map dim=0 (AKA batch dim) -> packed dim i.e. outer ragged dim - 1.
    # For other dims, subtract 1 to convert to inner space.
    return (
        # pyrefly: ignore [unsupported-operation]
        ragged_dim - 1 if dim == 0 else dim - 1
    )

