
def _parse_kstest_args(data1, data2, args, N):
    # kstest allows many different variations of arguments.
    # Pull out the parsing into a separate function
    # (xvals, yvals, )  # 2sample
    # (xvals, cdf function,..)
    # (xvals, name of distribution, ...)
    # (name of distribution, name of distribution, ...)

    # Returns xvals, yvals, cdf
    # where cdf is a cdf function, or None
    # and yvals is either an array_like of values, or None
    # and xvals is array_like.
    rvsfunc, cdf = None, None
    if isinstance(data1, str):
        rvsfunc = getattr(distributions, data1).rvs
    elif callable(data1):
        rvsfunc = data1

    if isinstance(data2, str):
        special_distributions = {'norm': special.ndtr}
        cdf = special_distributions.get(data2, getattr(distributions, data2).cdf)
        data2 = None
    elif callable(data2):
        cdf = data2
        data2 = None

    xp = array_namespace(data1, data2, *args)
    data1 = xp.sort(rvsfunc(*args, size=N) if rvsfunc else data1)
    return data1, data2, cdf

