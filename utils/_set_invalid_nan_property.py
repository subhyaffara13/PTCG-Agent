
def _set_invalid_nan_property(f):
    # Wrapper for input / output validation and standardization of distribution
    # functions that represent properties of the distribution itself:
    # logentropy, entropy
    # median, mode
    # moment
    # It ensures that the output is of the correct shape and dtype and that
    # there are NaNs wherever the distribution parameters were invalid.

    @functools.wraps(f)
    def filtered(self, *args, **kwargs):
        if self.validation_policy == _SKIP_ALL:
            return f(self, *args, **kwargs)

        res = f(self, *args, **kwargs)
        if res is None:
            # message could be more appropriate
            raise NotImplementedError(self._not_implemented)

        res = np.asarray(res)
        needs_copy = False
        dtype = res.dtype

        if dtype != self._dtype:  # this won't work for logmoments (complex)
            dtype = np.result_type(dtype, self._dtype)
            needs_copy = True

        if res.shape != self._shape:  # faster to check first
            res = np.broadcast_to(res, self._shape)
            needs_copy = needs_copy or self._any_invalid

        if needs_copy:
            res = res.astype(dtype=dtype, copy=True)

        if self._any_invalid:
            # may be redundant when quadrature is used, but not necessarily
            # when formulas are used.
            res[self._invalid] = np.nan

        return res[()]

    return filtered

