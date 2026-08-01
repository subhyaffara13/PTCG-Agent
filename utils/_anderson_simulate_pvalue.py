
def _anderson_simulate_pvalue(x, dist, method):
    message = ("The `___` attribute of a `MonteCarloMethod` object passed as the "
               "`method` parameter of `scipy.stats.anderson` is ignored.")

    method = method._asdict()
    if method.pop('rvs', False):
        warnings.warn(message.replace('___', 'rvs'), UserWarning, stacklevel=3)
    if method.pop('batch', False):
        warnings.warn(message.replace('___', 'batch'), UserWarning, stacklevel=3)
    method['n_mc_samples'] = method.pop('n_resamples')

    kwargs= {'known_params': {'loc': 0}} if dist == 'expon' else {}
    dist = getattr(stats, dist)
    res = stats.goodness_of_fit(dist, x, statistic='ad', **kwargs, **method)
    return res.pvalue

