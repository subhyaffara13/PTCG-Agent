
def xp_var(*args, **kwargs):
    kwargs.pop('_no_deco', None)
    return stats._stats_py._xp_var(*args, **kwargs)

