
def frexp_Tensor(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    output_kwargs = extract_kwargs(inp)

    mantissa, exponent = func(inp._values)
    return NestedTensor(mantissa, **output_kwargs), NestedTensor(
        exponent, **output_kwargs
    )

