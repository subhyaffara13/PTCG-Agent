
def trimmed_var(a, limits=(0.1,0.1), inclusive=(1,1), relative=True,
                axis=None, ddof=0):
    """Returns the trimmed variance of the data along the given axis.

    %s
    ddof : {0,integer}, optional
        Means Delta Degrees of Freedom. The denominator used during computations
        is (n-ddof). DDOF=0 corresponds to a biased estimate, DDOF=1 to an un-
        biased estimate of the variance.

    """  # numpydoc ignore=RT01
    if (not isinstance(limits,tuple)) and isinstance(limits,float):
        limits = (limits, limits)
    if relative:
        out = trimr(a,limits=limits, inclusive=inclusive,axis=axis)
    else:
        out = trima(a,limits=limits,inclusive=inclusive)

    return out.var(axis=axis, ddof=ddof)

