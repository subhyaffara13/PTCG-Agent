
def xp_mean_2samp(*args, **kwargs):
    kwargs.pop('_no_deco', None)
    weights = args[1]
    return stats._stats_py._xp_mean(args[0], *args[2:], weights=weights, **kwargs)

