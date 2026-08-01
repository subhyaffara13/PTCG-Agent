
def check_sample_meanvar_(popmean, popvar, sample, rng):
    if np.isfinite(popmean):
        check_sample_mean(sample, popmean)
    if np.isfinite(popvar):
        check_sample_var(sample, popvar, rng)

