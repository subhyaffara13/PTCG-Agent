
def use_two_step_variance(x, axis, keepdim):
    # two-step algorithm can get better performance in small reductions size
    # while it can accumulate more numerical error than Welford algorithm.
    axis = _validate_reduction_axis(x, axis)
    kwargs = _make_reduction_inner(
        x, axis=axis, keepdims=keepdim, dtype=None, override_return_dtype=None
    )

    ranges = kwargs["ranges"]
    reduction_numel = sympy_product(kwargs["reduction_ranges"])
    device = x.get_device()
    if not (device and device.type == "cpu"):
        threshold = config.unroll_reductions_threshold
    else:
        # 1024 is a default value to pass all the UTs about accuracy.
        # A larger threshold can still get performance benefits.
        threshold = config.cpp.use_two_step_variance_threshold
    return (
        isinstance(reduction_numel, sympy.Integer)
        and int(reduction_numel) <= threshold
        and sympy_product(ranges) != 1
    )

