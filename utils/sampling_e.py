
def sampling_E(expr, given_condition=None, library='scipy', numsamples=1,
               evalf=True, seed=None, **kwargs):
    """
    Sampling version of E.

    See Also
    ========

    P
    sampling_P
    sampling_density
    """
    samples = list(sample_iter(expr, given_condition, library=library,
                          numsamples=numsamples, seed=seed, **kwargs))
    result = Add(*samples) / numsamples

    if evalf:
        return result.evalf()
    else:
        return result

