
def _get_mwu_z(U, n1, n2, t, continuity=True, *, alternative, xp):
    '''Standardized MWU statistic'''
    # Follows mannwhitneyu [2]
    mu = n1 * n2 / 2
    n = n1 + n2

    # Tie correction according to [2], "Normal approximation and tie correction"
    # "A more computationally-efficient form..."
    tie_term = xp.sum(t**3 - t, axis=-1)
    s = xp.sqrt(n1*n2/12 * ((n + 1) - tie_term/(n*(n-1))))

    numerator = U - mu

    # Continuity correction.
    # Sign is chosen to always increase the p-value to account for the rest of the
    # probability mass _at_ q = U.
    if continuity:
        sign = _correction_sign(numerator, alternative, xp=xp)
        numerator -= 0.5 * sign

    # no problem evaluating the norm SF at an infinity
    with np.errstate(divide='ignore', invalid='ignore'):
        z = numerator / s
    return z

