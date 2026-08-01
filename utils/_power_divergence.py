
def _power_divergence(f_obs, f_exp, ddof, axis, lambda_, sum_check=True):
    xp = array_namespace(f_obs, f_exp, ddof)
    f_obs, f_exp, ddof = xp_promote(f_obs, f_exp, ddof,
                                    force_floating=True, xp=xp)

    # Convert the input argument `lambda_` to a numerical value.
    if isinstance(lambda_, str):
        if lambda_ not in _power_div_lambda_names:
            names = repr(list(_power_div_lambda_names.keys()))[1:-1]
            raise ValueError(f"invalid string for lambda_: {lambda_!r}. "
                             f"Valid strings are {names}")
        lambda_ = _power_div_lambda_names[lambda_]
    elif lambda_ is None:
        lambda_ = 1

    if f_exp is not None:
        # not sure why we force to float64, but not going to touch it
        f_obs_float = xp.asarray(f_obs, dtype=xp.float64)
        bshape = _broadcast_shapes((f_obs_float.shape, f_exp.shape))
        f_obs_float = xp.broadcast_to(f_obs_float, bshape)
        f_exp = xp.broadcast_to(f_exp, bshape)
        f_obs_float, f_exp = _share_masks(f_obs_float, f_exp, xp=xp)

        if sum_check:
            dtype_res = xp.result_type(f_obs.dtype, f_exp.dtype)
            rtol = xp.finfo(dtype_res).eps**0.5  # to pass existing tests
            with np.errstate(invalid='ignore'):
                f_obs_sum = xp.sum(f_obs_float, axis=axis, keepdims=True)
                f_exp_sum = xp.sum(f_exp, axis=axis, keepdims=True)
                relative_diff = (xp.abs(f_obs_sum - f_exp_sum) /
                                 xp.minimum(f_obs_sum, f_exp_sum))
                diff_gt_tol = xp.any(relative_diff > rtol, axis=axis, keepdims=True)

            if not is_lazy_array(diff_gt_tol) and xp.any(diff_gt_tol):
                msg = (f"For each axis slice, the sum of the observed "
                       f"frequencies must agree with the sum of the "
                       f"expected frequencies to a relative tolerance "
                       f"of {rtol}, but the percent differences are:\n"
                       f"{relative_diff}")
                raise ValueError(msg)
            elif is_lazy_array(diff_gt_tol):
                diff_gt_tol = xp.broadcast_to(diff_gt_tol, f_obs.shape)
                f_obs = xpx.at(f_obs)[diff_gt_tol].set(xp.nan)

    else:
        # Avoid warnings with the edge case of a data set with length 0
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f_exp = xp.mean(f_obs, axis=axis, keepdims=True)

    # `terms` is the array of terms that are summed along `axis` to create
    # the test statistic.  We use some specialized code for a few special
    # cases of lambda_.
    if lambda_ == 1:
        # Pearson's chi-squared statistic
        terms = (f_obs - f_exp)**2 / f_exp
    elif lambda_ == 0:
        # Log-likelihood ratio (i.e. G-test)
        terms = 2.0 * special.xlogy(f_obs, f_obs / f_exp)
    elif lambda_ == -1:
        # Modified log-likelihood ratio
        terms = 2.0 * special.xlogy(f_exp, f_exp / f_obs)
    else:
        # General Cressie-Read power divergence.
        terms = f_obs * ((f_obs / f_exp)**lambda_ - 1)
        terms /= 0.5 * lambda_ * (lambda_ + 1)

    stat = xp.sum(terms, axis=axis)

    num_obs = xp.asarray(_count_nonmasked(terms, axis), device=xp_device(terms),
                         dtype=f_obs.dtype)

    df = num_obs - 1 - ddof
    chi2 = _SimpleChi2(df)
    pvalue = _get_pvalue(stat, chi2 , alternative='greater', symmetric=False, xp=xp)

    stat = stat[()] if stat.ndim == 0 else stat
    pvalue = pvalue[()] if pvalue.ndim == 0 else pvalue

    return Power_divergenceResult(stat, pvalue)

