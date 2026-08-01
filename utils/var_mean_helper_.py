
def var_mean_helper_(x, *, axis, correction, keepdim, return_mean):
    out_dtype = x.get_dtype()
    compute_dtype = get_computation_dtype(out_dtype)
    x = to_dtype(x, compute_dtype, copy=False)
    kwargs = dict(
        x=x,
        axis=axis,
        correction=correction,
        keepdim=keepdim,
        return_mean=return_mean,
    )
    output = (
        var_mean_sum_(**kwargs)
        if (
            config.mtia.disable_welford_reduction
            or use_two_step_variance(x, axis=axis, keepdim=keepdim)
        )
        else var_mean_welford_(**kwargs)
    )
    output = tuple(to_dtype(x, out_dtype, copy=False) for x in output)
    return output[0] if not return_mean else output

