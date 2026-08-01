
def jagged_unary_pointwise(func, *args, **kwargs):
    # assume if we get here that there is a single NJT input in the args
    njt = next(arg for arg in args if isinstance(arg, NestedTensor))
    return NestedTensor(
        func(*(arg._values if arg is njt else arg for arg in args), **kwargs),
        **extract_kwargs(njt),
    )

