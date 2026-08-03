import functools

def _cdf2_input_validation(f):
    # Wrapper that does the job of `_set_invalid_nan` when `cdf` or `logcdf`
    # is called with two quantile arguments.
    # Let's keep it simple; no special cases for speed right now.
    # The strategy is a bit different than for 1-arg `cdf` (and other methods
    # covered by `_set_invalid_nan`). For 1-arg `cdf`, elements of `x` that
    # are outside (or at the edge of) the support get replaced by `nan`,
    # and then the results get replaced by the appropriate value (0 or 1).
    # We *could* do something similar, dispatching to `_cdf1` in these
    # cases. That would be a bit more robust, but it would also be quite
    # a bit more complex, since we'd have to do different things when
    # `x` and `y` are both out of bounds, when just `x` is out of bounds,
    # when just `y` is out of bounds, and when both are out of bounds.
    # I'm not going to do that right now. Instead, simply replace values
    # outside the support by those at the edge of the support. Here, we also
    # omit some of the optimizations that make `_set_invalid_nan` faster for
    # simple arguments (e.g. float64 scalars).

    @functools.wraps(f)
    def wrapped(self, x, y, *args, **kwargs):
        func_name = f.__name__

        low, high = self.support()
        x, y, low, high = np.broadcast_arrays(x, y, low, high)
        dtype = np.result_type(x.dtype, y.dtype, self._dtype)
        # yes, copy to avoid modifying input arrays
        x, y = x.astype(dtype, copy=True), y.astype(dtype, copy=True)

        # Swap arguments to ensure that x < y, and replace
        # out-of domain arguments with domain endpoints. We'll
        # transform the result later.
        i_swap = y < x
        x[i_swap], y[i_swap] = y[i_swap], x[i_swap]
        i = x < low
        x[i] = low[i]
        i = y < low
        y[i] = low[i]
        i = x > high
        x[i] = high[i]
        i = y > high
        y[i] = high[i]

        res = f(self, x, y, *args, **kwargs)

        # Clipping probability to [0, 1]
        if func_name in {'_cdf2', '_ccdf2'}:
            res = np.clip(res, 0., 1.)
        else:
            res = np.clip(res, None, 0.)  # exp(res) < 1

        # Transform the result to account for swapped argument order
        res = np.asarray(res)
        if func_name == '_cdf2':
            res[i_swap] *= -1.
        elif func_name == '_ccdf2':
            res[i_swap] *= -1
            res[i_swap] += 2.
        elif func_name == '_logcdf2':
            res = np.asarray(res + 0j) if np.any(i_swap) else res
            res[i_swap] = res[i_swap] + np.pi*1j
        else:
            # res[i_swap] is always positive and less than 1, so it's
            # safe to ensure that the result is real
            res[i_swap] = _logexpxmexpy(np.log(2), res[i_swap]).real
        return res[()]

    return wrapped

