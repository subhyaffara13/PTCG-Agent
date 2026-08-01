
def permute_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    inp = new_kwargs.pop("input")
    dims = new_kwargs.pop("dims")
    inp_kwargs = extract_kwargs(inp)
    inp_dim = len(inp._size)

    # The first two checks are the same as the checks in the normal permute implementation
    if inp_dim != len(dims):
        raise ValueError(
            f"permute(): number of dimensions in the tensor input ({inp_dim}) "
            + f"does not match the length of the desired ordering of dimensions ({len(dims)}).",
        )

    from torch._prims_common import canonicalize_dims

    canonicalized_dims = canonicalize_dims(inp_dim, dims)

    if len(canonicalized_dims) != len(set(canonicalized_dims)):
        raise ValueError("permute(): duplicate dims are not allowed.")

    if inp._lengths is not None:
        raise ValueError(
            "permute(): not supported on jagged layout nested tensor with holes"
        )
    if canonicalized_dims[0] != 0:
        raise ValueError(
            "Permute is not supported on the batch dimension for jagged NT"
        )
    inp_kwargs["_ragged_idx"] = canonicalized_dims.index(inp._ragged_idx)
    inner_dims = [
        _outer_to_inner_dim(inp_dim, dim, inp._ragged_idx)
        for dim in canonicalized_dims[1:]
    ]
    new_kwargs["dims"] = inner_dims
    return NestedTensor(func(inp._values, **new_kwargs), **inp_kwargs)

