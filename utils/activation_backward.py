
def activation_backward(func, *args, **kwargs):
    # first NJT arg is expected to be grad_output
    grad_output = next(arg for arg in args if isinstance(arg, NestedTensor))
    return NestedTensor(
        func(
            *(arg._values if isinstance(arg, NestedTensor) else arg for arg in args),
            **kwargs,
        ),
        **extract_kwargs(grad_output),
    )

