
def _wilcoxon_nd(x, y=None, zero_method='wilcox', correction=True,
                 alternative='two-sided', method='auto', axis=0):

    temp = _wilcoxon_iv(x, y, zero_method, correction, alternative, method, axis)
    d, zero_method, correction, alternative, method, axis, output_z, n_zero, xp = temp

    if xp_size(d) == 0:
        NaN = _get_nan(d, xp=xp)
        res = _morestats.WilcoxonResult(statistic=NaN, pvalue=NaN)
        if method == 'asymptotic':
            res.zstatistic = NaN
        return res

    r_plus, r_minus, se, z, count, has_ties = _wilcoxon_statistic(
        d, method, zero_method, xp=xp
    )

    # we only know if there are ties after computing the statistic and not
    # at the input validation stage. if the original method was auto and
    # the decision was to use an exact test, we override this to
    # a permutation test now (since method='exact' is not exact in the
    # presence of ties)
    if method == "auto":
        if not (has_ties or n_zero > 0):
            method = "exact"
        elif d.shape[-1] <= 13:
            # the possible outcomes to be simulated by the permutation test
            # are 2**n, where n is the sample size.
            # if n <= 13, the p-value is deterministic since 2**13 is less
            # than 9999, the default number of n_resamples
            method = stats.PermutationMethod()
        else:
            # if there are ties and the sample size is too large to
            # run a deterministic permutation test, fall back to asymptotic
            method = "asymptotic"

    if method == 'asymptotic':
        if correction:
            sign = _correction_sign(z, alternative, xp=xp)
            z = xpx.at(z)[...].subtract(sign * 0.5 / se)
        p = _get_pvalue(z, _SimpleNormal(), alternative, xp=xp)
    elif method == 'exact':
        dist = WilcoxonDistribution(count)
        # The null distribution in `dist` is exact only if there are no ties
        # or zeros. If there are ties or zeros, the statistic can be non-
        # integral, but the null distribution is only defined for integral
        # values of the statistic. Therefore, we're conservative: round
        # non-integral statistic up before computing CDF and down before
        # computing SF. This preserves symmetry w.r.t. alternatives and
        # order of the input arguments. See gh-19872.
        r_plus_np = np.asarray(r_plus)
        if alternative == 'less':
            p = dist.cdf(np.ceil(r_plus_np))
        elif alternative == 'greater':
            p = dist.sf(np.floor(r_plus_np))
        else:
            p = 2 * np.minimum(dist.sf(np.floor(r_plus_np)),
                               dist.cdf(np.ceil(r_plus_np)))
            p = np.clip(p, 0, 1)
        p = xp.asarray(p, dtype=d.dtype)
    else:  # `PermutationMethod` instance (already validated)
        p = stats.permutation_test(
            # permutation_test always uses `axis=-1` as `_wilcoxon_statistic` assumes
            (d,), lambda d, axis: _wilcoxon_statistic(d, method, zero_method, xp=xp)[0],
            permutation_type='samples', **method._asdict(),
            alternative=alternative, axis=-1).pvalue

    # for backward compatibility...
    statistic = xp.minimum(r_plus, r_minus) if alternative=='two-sided' else r_plus
    z = -xp.abs(z) if (alternative == 'two-sided' and method == 'asymptotic') else z

    statistic = statistic[()] if statistic.ndim == 0 else statistic
    p = p[()] if p.ndim == 0 else p
    res = _morestats.WilcoxonResult(statistic=statistic, pvalue=p)
    if output_z:
        res.zstatistic = z[()] if z.ndim == 0 else z
    return res

