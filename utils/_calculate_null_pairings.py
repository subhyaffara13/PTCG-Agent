import math


def _calculate_null_pairings(data, statistic, n_permutations, batch,
                             rng=None, *, xp):
    """
    Calculate null distribution for association tests.
    """
    n_samples = len(data)

    # compute number of permutations (factorial(n) permutations of each sample)
    n_obs_sample = data[0].shape[-1]  # observations per sample; same for each
    n_max = math.factorial(n_obs_sample)**n_samples

    # `perm_generator` is an iterator that produces a list of permutations of
    # indices from 0 to n_obs_sample, one for each sample.
    if n_permutations >= n_max:
        exact_test = True
        n_permutations = n_max
        batch = batch or int(n_permutations)
        # Cartesian product of the sets of all permutations of indices
        perm_generator = product(*(permutations(range(n_obs_sample))
                                   for i in range(n_samples)))
        batched_perm_generator = _batch_generator(perm_generator, batch=batch)
    else:
        exact_test = False
        batch = batch or int(n_permutations)
        # Separate random permutations of indices for each sample.
        # Again, it would be nice if RandomState/Generator.permutation
        # could permute each axis-slice separately.
        args = n_permutations, n_samples, n_obs_sample, batch, rng
        batched_perm_generator = _pairings_permutations_gen(*args)

    null_distribution = []

    for indices in batched_perm_generator:
        indices = xp.asarray(indices)

        # `indices` is 3D: the zeroth axis is for permutations, the next is
        # for samples, and the last is for observations. Swap the first two
        # to make the zeroth axis correspond with samples, as it does for
        # `data`.
        indices = xp_swapaxes(indices, 0, 1, xp=xp)

        # When we're done, `data_batch` will be a list of length `n_samples`.
        # Each element will be a batch of random permutations of one sample.
        # The zeroth axis of each batch will correspond with permutations,
        # and the last will correspond with observations. (This makes it
        # easy to pass into `statistic`.)
        data_batch = [None]*n_samples
        for i in range(n_samples):
            # data_batch[i] = data[i][..., indices[i]]
            data_batch[i] = _get_from_last_axis(data[i], indices[i, ...], xp=xp)
            data_batch[i] = xp.moveaxis(data_batch[i], -2, 0)

        null_distribution.append(statistic(*data_batch, axis=-1))
    null_distribution = xp.concat(null_distribution, axis=0)

    return null_distribution, n_permutations, exact_test

