
def amax_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    dtype = new_kwargs["input"].dtype
    dtype_min = _get_padding_value(dtype, "min")
    return _apply_reduction(func, "amax", dtype_min, *args, **kwargs)

