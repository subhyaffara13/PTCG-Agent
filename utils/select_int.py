
def select_int(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    new_kwargs["dim"], operating_on_batch = _wrap_jagged_dim(
        inp.dim(), new_kwargs["dim"], inp._ragged_idx, "select", allow_batch_dim=True
    )

    # handle batch dim slicing via unbind() for now
    # TODO: make this more efficient
    if operating_on_batch:
        return inp.unbind()[new_kwargs["index"]]

    if inp._lengths is not None:
        raise ValueError(
            "select(): not yet supported on dim != 0 for non-contiguous nested tensor with holes"
        )

    # if selecting before the ragged dim, adjust output ragged_idx
    out_kwargs = extract_kwargs(inp)
    if new_kwargs["dim"] < inp._ragged_idx - 1:
        out_kwargs["_ragged_idx"] -= 1

    return NestedTensor(func(inp._values, **new_kwargs), **out_kwargs)

