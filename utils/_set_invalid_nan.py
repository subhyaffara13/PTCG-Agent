import functools

def _set_invalid_nan(f):
    # Wrapper for input / output validation and standardization of distribution
    # functions that accept either the quantile or percentile as an argument:
    # logpdf, pdf
    # logpmf, pmf
    # logcdf, cdf
    # logccdf, ccdf
    # ilogcdf, icdf
    # ilogccdf, iccdf
    # Arguments that are outside the required range are replaced by NaN before
    # passing them into the underlying function. The corresponding outputs
    # are replaced by the appropriate value before being returned to the user.
    # For example, when the argument of `cdf` exceeds the right end of the
    # distribution's support, the wrapper replaces the argument with NaN,
    # ignores the output of the underlying function, and returns 1.0. It also
    # ensures that output is of the appropriate shape and dtype.

    endpoints = {'icdf': (0, 1), 'iccdf': (0, 1),
                 'ilogcdf': (-np.inf, 0), 'ilogccdf': (-np.inf, 0)}
    replacements = {'logpdf': (-inf, -inf), 'pdf': (0, 0),
                    'logpmf': (-inf, -inf), 'pmf': (0, 0),
                    '_logcdf1': (-inf, 0), '_logccdf1': (0, -inf),
                    '_cdf1': (0, 1), '_ccdf1': (1, 0)}
    replace_strict = {'pdf', 'logpdf', 'pmf', 'logpmf'}
    replace_exact = {'icdf', 'iccdf', 'ilogcdf', 'ilogccdf'}
    clip = {'_cdf1', '_ccdf1'}
    clip_log = {'_logcdf1', '_logccdf1'}
    # relevant to discrete distributions only
    replace_non_integral = {'pmf', 'logpmf', 'pdf', 'logpdf'}

    @functools.wraps(f)
    def filtered(self, x, *args, **kwargs):
        if self.validation_policy == _SKIP_ALL:
            return f(self, x, *args, **kwargs)

        method_name = f.__name__
        x = np.asarray(x)
        dtype = self._dtype
        shape = self._shape
        discrete = isinstance(self, DiscreteDistribution)
        keep_low_endpoint = discrete and method_name in {'_cdf1', '_logcdf1',
                                                         '_ccdf1', '_logccdf1'}

        # Ensure that argument is at least as precise as distribution
        # parameters, which are already at least floats. This will avoid issues
        # with raising integers to negative integer powers and failure to replace
        # invalid integers with NaNs.
        if x.dtype != dtype:
            dtype = np.result_type(x.dtype, dtype)
            x = np.asarray(x, dtype=dtype)

        # Broadcasting is slow. Do it only if necessary.
        if not x.shape == shape:
            try:
                shape = np.broadcast_shapes(x.shape, shape)
                x = np.broadcast_to(x, shape)
                # Should we broadcast the distribution parameters to this shape, too?
            except ValueError as e:
                message = (
                    f"The argument provided to `{self.__class__.__name__}"
                    f".{method_name}` cannot be be broadcast to the same "
                    "shape as the distribution parameters.")
                raise ValueError(message) from e

        low, high = endpoints.get(method_name, self.support())

        # Check for arguments outside of domain. They'll be replaced with NaNs,
        # and the result will be set to the appropriate value.
        left_inc, right_inc = self._variable.domain.inclusive
        mask_low = (x < low if (method_name in replace_strict and left_inc)
                    or keep_low_endpoint else x <= low)
        mask_high = (x > high if (method_name in replace_strict and right_inc)
                     else x >= high)
        mask_invalid = (mask_low | mask_high)
        any_invalid = (mask_invalid if mask_invalid.shape == ()
                       else np.any(mask_invalid))

        # Check for arguments at domain endpoints, whether they
        # are part of the domain or not.
        any_endpoint = False
        if method_name in replace_exact:
            mask_low_endpoint = (x == low)
            mask_high_endpoint = (x == high)
            mask_endpoint = (mask_low_endpoint | mask_high_endpoint)
            any_endpoint = (mask_endpoint if mask_endpoint.shape == ()
                            else np.any(mask_endpoint))

        # Check for non-integral arguments to PMF method
        # or PDF of a discrete distribution.
        any_non_integral = False
        if discrete and method_name in replace_non_integral:
            mask_non_integral = (x != np.floor(x))
            any_non_integral = (mask_non_integral if mask_non_integral.shape == ()
                                else np.any(mask_non_integral))

        # Set out-of-domain arguments to NaN. The result will be set to the
        # appropriate value later.
        if any_invalid:
            x = np.array(x, dtype=dtype, copy=True)
            x[mask_invalid] = np.nan

        res = np.asarray(f(self, x, *args, **kwargs))

        # Ensure that the result is the correct dtype and shape,
        # copying (only once) if necessary.
        res_needs_copy = False
        if res.dtype != dtype:
            dtype = np.result_type(dtype, self._dtype)
            res_needs_copy = True

        if res.shape != shape:  # faster to check first
            res = np.broadcast_to(res, self._shape)
            res_needs_copy = (res_needs_copy or any_invalid
                              or any_endpoint or any_non_integral)

        if res_needs_copy:
            res = np.array(res, dtype=dtype, copy=True)

        # For non-integral arguments to PMF (and PDF of discrete distribution)
        # replace with zero.
        if any_non_integral:
            zero = -np.inf if method_name in {'logpmf', 'logpdf'} else 0
            res[mask_non_integral & ~np.isnan(res)] = zero

        # For arguments outside the function domain, replace results
        if any_invalid:
            replace_low, replace_high = (
                replacements.get(method_name, (np.nan, np.nan)))
            res[mask_low] = replace_low
            res[mask_high] = replace_high

        # For arguments at the endpoints of the domain, replace results
        if any_endpoint:
            a, b = self.support()
            if a.shape != shape:
                a = np.array(np.broadcast_to(a, shape), copy=True)
                b = np.array(np.broadcast_to(b, shape), copy=True)

            replace_low_endpoint = (
                b[mask_low_endpoint] if method_name.endswith('ccdf')
                else a[mask_low_endpoint])
            replace_high_endpoint = (
                a[mask_high_endpoint] if method_name.endswith('ccdf')
                else b[mask_high_endpoint])

            if not keep_low_endpoint:
                res[mask_low_endpoint] = replace_low_endpoint
            res[mask_high_endpoint] = replace_high_endpoint

        # Clip probabilities to [0, 1]
        if method_name in clip:
            res = np.clip(res, 0., 1.)
        elif method_name in clip_log:
            res = res.real  # exp(res) > 0
            res = np.clip(res, None, 0.)  # exp(res) < 1

        return res[()]

    return filtered

