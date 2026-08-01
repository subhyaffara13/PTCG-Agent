
def _percentile_of_score(a, score, axis, xp):
    """Vectorized, simplified `scipy.stats.percentileofscore`.
    Uses logic of the 'mean' value of percentileofscore's kind parameter.

    Unlike `stats.percentileofscore`, the percentile returned is a fraction
    in [0, 1].
    """
    B = a.shape[axis]
    nonzeros = (xp.count_nonzero(a < score, axis=axis)
                + xp.count_nonzero(a <= score, axis=axis))
    return xp.astype(nonzeros, score.dtype) / (2 * B)

