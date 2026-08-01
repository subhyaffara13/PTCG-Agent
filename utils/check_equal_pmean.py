
def check_equal_pmean(*args, **kwargs):
    return check_equal_xmean(*args, mean_fun=stats.pmean, **kwargs)

