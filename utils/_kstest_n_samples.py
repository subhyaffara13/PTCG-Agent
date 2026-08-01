
def _kstest_n_samples(kwargs):
    cdf = kwargs['cdf']
    return 1 if (isinstance(cdf, str) or callable(cdf)) else 2

