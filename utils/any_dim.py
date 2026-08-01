
def any_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    # wrap dim in list to redispatch to dims overload
    new_kwargs["dim"] = [new_kwargs["dim"]]
    return any_dims(torch.ops.aten.any.dims, **new_kwargs)

