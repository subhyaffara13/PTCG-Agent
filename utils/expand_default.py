
def expand_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    size = new_kwargs["size"]

    if "implicit" in new_kwargs and new_kwargs.pop("implicit"):
        raise AssertionError("implicit expand is not supported")
    if not raggedness_matches(inp, size):
        raise RuntimeError(f"expand(): cannot expand shape {inp._size} -> {size}")

    expand_arg = [-1 if d == inp._ragged_idx else size[d] for d in range(1, inp.dim())]
    return NestedTensor(func(inp._values, expand_arg), **extract_kwargs(inp))

