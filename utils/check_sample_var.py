
def check_sample_var(sample, popvar, rng):
    # check that population mean lies within the CI bootstrapped from the
    # sample. This used to be a chi-squared test for variance, but there were
    # too many false positives
    res = stats.bootstrap(
        (sample,),
        lambda x, axis: x.var(ddof=1, axis=axis),
        confidence_level=0.995,
        rng=rng,
    )
    conf = res.confidence_interval
    low, high = conf.low, conf.high
    assert low <= popvar <= high

