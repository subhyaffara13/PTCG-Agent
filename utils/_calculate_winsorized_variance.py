
def _calculate_winsorized_variance(a, g, axis, *, xp):
    """Calculates g-times winsorized variance along specified axis"""
    # it is expected that the input `a` is sorted along the correct axis
    if g == 0:
        return _var(a, ddof=1, axis=axis, xp=xp)
    # move the intended axis to the end that way it is easier to manipulate
    a_win = xp.moveaxis(a, axis, -1)

    # save where NaNs are for later use.
    nans_indices = xp.any(xp.isnan(a_win), axis=-1)

    # Winsorization and variance calculation are done in one step in [4]
    # (1-3), but here winsorization is done first; replace the left and
    # right sides with the repeating value. This can be see in effect in (
    # 1-3) in [4], where the leftmost and rightmost tails are replaced with
    # `(g + 1) * x_{g + 1}` on the left and `(g + 1) * x_{n - g}` on the
    # right. Zero-indexing turns `g + 1` to `g`, and `n - g` to `- g - 1` in
    # array indexing.
    a_win = xpx.at(a_win)[..., :g].set(a_win[..., g:g+1])
    a_win = xpx.at(a_win)[..., -g:].set(a_win[..., -g - 1:-g])

    # Determine the variance. In [4], the degrees of freedom is expressed as
    # `h - 1`, where `h = n - 2g` (unnumbered equations in Section 1, end of
    # page 369, beginning of page 370). This is converted to NumPy's format,
    # `n - ddof` for use with `np.var`. The result is converted to an
    # array to accommodate indexing later.
    var_win = xp.asarray(_var(a_win, ddof=(2 * g + 1), axis=-1, xp=xp))

    # with `nan_policy='propagate'`, NaNs may be completely trimmed out
    # because they were sorted into the tail of the array. In these cases,
    # replace computed variances with `np.nan`.
    var_win = xpx.at(var_win)[nans_indices].set(xp.nan)
    return var_win

