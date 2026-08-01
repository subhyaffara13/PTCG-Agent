
def sampling_P(condition, given_condition=None, library='scipy', numsamples=1,
               evalf=True, seed=None, **kwargs):
    """
    Sampling version of P.

    See Also
    ========

    P
    sampling_E
    sampling_density

    """

    count_true = 0
    count_false = 0
    samples = sample_iter(condition, given_condition, library=library,
                          numsamples=numsamples, seed=seed, **kwargs)

    for sample in samples:
        if sample:
            count_true += 1
        else:
            count_false += 1

    result = S(count_true) / numsamples
    if evalf:
        return result.evalf()
    else:
        return result

