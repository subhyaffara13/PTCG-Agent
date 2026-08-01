
def squeeze_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    values = inp._values

    new_kwargs["dim"] = _wrap_jagged_dim(
        len(inp._size), new_kwargs["dim"], inp._ragged_idx, "squeeze"
    )
    return NestedTensor(func(values, **new_kwargs), **extract_kwargs(inp))

