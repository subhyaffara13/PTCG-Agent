
def _get_pvalue(statistic, distribution, alternative, symmetric=True, xp=None):
    """Get p-value given the statistic, (continuous) distribution, and alternative"""
    xp = array_namespace(statistic) if xp is None else xp

    if alternative == 'less':
        pvalue = distribution.cdf(statistic)
    elif alternative == 'greater':
        pvalue = distribution.sf(statistic)
    elif alternative == 'two-sided':
        pvalue = 2 * (distribution.sf(xp.abs(statistic)) if symmetric
                      else xp.minimum(distribution.cdf(statistic),
                                      distribution.sf(statistic)))
    else:
        message = "`alternative` must be 'less', 'greater', or 'two-sided'."
        raise ValueError(message)

    return pvalue

