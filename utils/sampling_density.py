
def sampling_density(expr, given_condition=None, library='scipy',
                    numsamples=1, seed=None, **kwargs):
    """
    Sampling version of density.

    See Also
    ========
    density
    sampling_P
    sampling_E
    """

    results = {}
    for result in sample_iter(expr, given_condition, library=library,
                              numsamples=numsamples, seed=seed, **kwargs):
        results[result] = results.get(result, 0) + 1

    return results

