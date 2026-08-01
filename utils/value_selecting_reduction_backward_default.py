
def value_selecting_reduction_backward_default(func, *args, **kwargs):
    from torch.fx.experimental.symbolic_shapes import is_nested_int

    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    grad = new_kwargs.pop("grad")
    new_kwargs["grad"] = grad._values
    indices = new_kwargs.pop("indices")
    new_kwargs["indices"] = indices._values
    # should always succeed; sizes should contain a nested int
    ragged_idx = next(i for i, s in enumerate(new_kwargs["sizes"]) if is_nested_int(s))
    # convert dim -> values-space dim
    new_kwargs["dim"] = _wrap_jagged_dim(
        len(new_kwargs["sizes"]),
        new_kwargs["dim"],
        ragged_idx,
        "value_selecting_reduction_backward",
    )
    # convert saved NJT sizes -> values-space sizes
    sizes = new_kwargs.pop("sizes")
    sizes[ragged_idx] = indices._values.size(indices._ragged_idx - 1)
    sizes = sizes[1:]
    new_kwargs["sizes"] = sizes

    output_kwargs = extract_kwargs(indices)
    output_kwargs["_ragged_idx"] = ragged_idx

    return NestedTensor(func(**new_kwargs), **output_kwargs)

