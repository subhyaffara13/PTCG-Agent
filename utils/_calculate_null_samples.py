
def _calculate_null_samples(data, statistic, n_permutations, batch,
                            rng=None, *, xp):
    """
    Calculate null distribution for paired-sample tests.
    """
    n_samples = len(data)

    # By convention, the meaning of the "samples" permutations type for
    # data with only one sample is to flip the sign of the observations.
    # Achieve this by adding a second sample - the negative of the original.
    if n_samples == 1:
        data = [data[0], -data[0]]

    # The "samples" permutation strategy is the same as the "pairings"
    # strategy except the roles of samples and observations are flipped.
    # So swap these axes, then we'll use the function for the "pairings"
    # strategy to do all the work!
    data = xp.stack(data, axis=0)
    data = xp_swapaxes(data, 0, -1, xp=xp)

    # (Of course, the user's statistic doesn't know what we've done here,
    # so we need to pass it what it's expecting.)
    def statistic_wrapped(*data, axis):
        # can we do this without converting back and forth between
        # array and list?
        data = xp.stack(data, axis=0)
        data = xp_swapaxes(data, 0, -1, xp=xp)
        if n_samples == 1:
            data = data[0:1, ...]
        data = [data[i, ...] for i in range(data.shape[0])]
        return statistic(*data, axis=axis)

    data = [data[i, ...] for i in range(data.shape[0])]
    return _calculate_null_pairings(data, statistic_wrapped, n_permutations,
                                    batch, rng, xp=xp)

