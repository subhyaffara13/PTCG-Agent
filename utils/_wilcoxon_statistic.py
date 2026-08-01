
def _wilcoxon_statistic(d, method, zero_method='wilcox', *, xp):
    dtype = d.dtype
    i_zeros = (d == 0)

    if zero_method == 'wilcox':
        # Wilcoxon's method for treating zeros was to remove them from
        # the calculation. We do this by replacing 0s with NaNs, which
        # are ignored anyway.
        # Copy required for array-api-strict. See data-apis/array-api-extra#506.
        d = xpx.at(d)[i_zeros].set(xp.nan, copy=True)

    i_nan = xp.isnan(d)
    n_nan = xp.astype(xp.count_nonzero(i_nan, axis=-1), dtype)
    count = _count_nonmasked(d, axis=-1) - n_nan

    r, _, t = _rankdata(xp.abs(d), 'average', return_ties=True, xp=xp)
    r, t = xp.astype(r, dtype, copy=False), xp.astype(t, dtype, copy=False)

    r_plus = xp.sum(xp.astype(d > 0, dtype) * r, axis=-1)
    r_minus = xp.sum(xp.astype(d < 0, dtype) * r, axis=-1)

    has_ties = xp.any(t == 0)

    if zero_method == "zsplit":
        # The "zero-split" method for treating zeros is to add half their contribution
        # to r_plus and half to r_minus.
        # See gh-2263 for the origin of this method.
        r_zero_2 = xp.sum(xp.astype(i_zeros, dtype) * r, axis=-1) / 2
        r_plus = xpx.at(r_plus)[...].add(r_zero_2)
        r_minus = xpx.at(r_minus)[...].add(r_zero_2)

    mn = count * (count + 1.) * 0.25
    se = count * (count + 1.) * (2. * count + 1.)

    if zero_method == "pratt":
        # Pratt's method for treating zeros was just to modify the z-statistic.

        # normal approximation needs to be adjusted, see Cureton (1967)
        n_zero = xp.astype(xp.count_nonzero(i_zeros, axis=-1), dtype)
        mn = xpx.at(mn)[...].subtract(n_zero * (n_zero + 1.) * 0.25)
        se = xpx.at(se)[...].subtract(n_zero * (n_zero + 1.) * (2. * n_zero + 1.))

        # zeros are not to be included in tie-correction.
        # any tie counts corresponding with zeros are in the 0th column
        # t[xp.any(i_zeros, axis=-1), 0] = 0
        t_i_zeros = xp.zeros_like(i_zeros)
        t_i_zeros = xpx.at(t_i_zeros)[..., 0].set(xp.any(i_zeros, axis=-1))
        t = xpx.at(t)[t_i_zeros].set(0.)

    tie_correct = xp.sum(t**3 - t, axis=-1)
    se = xp.sqrt((se - tie_correct/2) / 24)

    # se = 0 means that no non-zero values are left in d. we only need z
    # if method is asymptotic. however, if method="auto", the switch to
    # asymptotic might only happen after the statistic is calculated, so z
    # needs to be computed. in all other cases, avoid division by zero warning
    # (z is not needed anyways)
    if method in ["asymptotic", "auto"]:
        z = (r_plus - mn) / se
    else:
        z = xp.nan

    return r_plus, r_minus, se, z, count, has_ties

