
def _softmax_backward(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )
    grad_out = new_kwargs.pop("grad_output")
    output = new_kwargs.pop("output")
    return NestedTensor(
        func(grad_out._values, output._values, **new_kwargs), **extract_kwargs(grad_out)
    )

