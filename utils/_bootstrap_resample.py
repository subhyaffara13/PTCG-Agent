
def _bootstrap_resample(sample, n_resamples=None, rng=None, *, xp):
    """Bootstrap resample the sample."""
    n = sample.shape[-1]

    # bootstrap - each row is a random resample of original observations
    i = rng_integers(rng, 0, n, (n_resamples, n))

    i = xp.asarray(i, device=xp_device(sample))
    return _get_from_last_axis(sample, i, xp=xp)

