
def reduce_scatter_with_assert(
    cls,
    orig_reduce_scatter: Callable,
    assert_fn: Callable,  # `assert_fn(output: Tensor)`
    *args: Any,
    **kwargs: Any,
):
    if len(args) > 0:
        output = args[0]
    elif "output" in kwargs:
        output = kwargs["output"]
    else:
        raise AssertionError(
            f"Cannot get reduce-scatter output from\nargs: {args}\nkwargs: {kwargs}"
        )
    assert_fn(output)
    return orig_reduce_scatter(*args, **kwargs)

