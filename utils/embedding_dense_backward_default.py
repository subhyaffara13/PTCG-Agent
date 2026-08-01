
def embedding_dense_backward_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    indices = new_kwargs.pop("indices")
    grad_output = new_kwargs.pop("grad_output")
    return func(grad_output._values, indices._values, **new_kwargs)

