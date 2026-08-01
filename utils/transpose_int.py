
def transpose_int(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    from torch._prims_common import canonicalize_dims

    inp = new_kwargs.pop("input")
    dim0, dim1 = canonicalize_dims(inp.dim(), (new_kwargs["dim0"], new_kwargs["dim1"]))

    # To support the SDPA API, inputs need to have the ragged idx transposed to dim 2
    # instead of 1, although the internal Flash and mem-effn implementations will
    # use the inputs with raggedness in dim 1.
    if dim0 == inp._ragged_idx or dim1 == inp._ragged_idx:
        if dim0 == 0 or dim1 == 0:
            raise ValueError(
                "Transpose is not supported on the batch dimension for jagged NT"
            )
        if dim0 == inp._ragged_idx:
            to_dim = dim1
        else:
            to_dim = dim0
        inp_kwargs = extract_kwargs(inp)
        inp_kwargs["_ragged_idx"] = to_dim
        return NestedTensor(
            inp.values().transpose(
                _outer_to_inner_dim(len(inp._size), dim0, inp._ragged_idx),
                _outer_to_inner_dim(len(inp._size), dim1, inp._ragged_idx),
            ),
            **inp_kwargs,
        )

    new_kwargs["dim0"] = _wrap_jagged_dim(
        inp.dim(), new_kwargs["dim0"], inp._ragged_idx, "transpose"
    )
    new_kwargs["dim1"] = _wrap_jagged_dim(
        inp.dim(), new_kwargs["dim1"], inp._ragged_idx, "transpose"
    )

    return NestedTensor(func(inp._values, **new_kwargs), **extract_kwargs(inp))

