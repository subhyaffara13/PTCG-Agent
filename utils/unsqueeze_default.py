
def unsqueeze_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    values = inp._values

    # Account for collapsed jagged dim
    dim = new_kwargs["dim"]
    new_kwargs["dim"] = _wrap_jagged_dim(
        len(inp._size) + 1, dim, inp._ragged_idx, "unsqueeze", allow_ragged_dim=True
    )

    # ragged_idx changes if a dimension is added before it
    output_kwargs = extract_kwargs(inp)
    if new_kwargs["dim"] <= inp._ragged_idx - 1:
        output_kwargs["_ragged_idx"] += 1

    return NestedTensor(func(values, **new_kwargs), **output_kwargs)

