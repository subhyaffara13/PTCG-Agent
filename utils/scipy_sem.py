
def scipy_sem(*args, **kwargs):
    from scipy.stats import sem

    return sem(*args, ddof=1, **kwargs)

