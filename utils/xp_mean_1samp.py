
def xp_mean_1samp(*args, **kwargs):
    kwargs.pop('_no_deco', None)
    return stats._stats_py._xp_mean(*args, **kwargs)

