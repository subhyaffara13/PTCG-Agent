import math


def _calculate_null_both(data, statistic, n_permutations, batch,
                         rng=None, *, xp):
    """
    Calculate null distribution for independent sample tests.
    """
    # compute number of permutations
    # (distinct partitions of data into samples of these sizes)
    n_obs_i = [sample.shape[-1] for sample in data]  # observations per sample
    n_obs_ic = list(accumulate(n_obs_i, initial=0))
    n_obs = n_obs_ic[-1]  # total number of observations
    n_max = math.prod([math.comb(n, k) for n, k in zip(n_obs_ic[1:], n_obs_ic[:-1])])

    # perm_generator is an iterator that produces permutations of indices
    # from 0 to n_obs. We'll concatenate the samples, use these indices to
    # permute the data, then split the samples apart again.
    if n_permutations >= n_max:
        exact_test = True
        n_permutations = n_max
        perm_generator = _all_partitions_concatenated(n_obs_i)
    else:
        exact_test = False
        # Neither RandomState.permutation nor Generator.permutation
        # can permute axis-slices independently. If this feature is
        # added in the future, batches of the desired size should be
        # generated in a single call.
        perm_generator = (rng.permutation(n_obs)
                          for i in range(n_permutations))

    batch = batch or int(n_permutations)
    null_distribution = []

    # First, concatenate all the samples. In batches, permute samples with
    # indices produced by the `perm_generator`, split them into new samples of
    # the original sizes, compute the statistic for each batch, and add these
    # statistic values to the null distribution.
    data = xp.concat(data, axis=-1)
    for indices in _batch_generator(perm_generator, batch=batch):
        # Creating a tensor from a list of numpy.ndarrays is extremely slow...
        indices = np.asarray(indices)
        indices = xp.asarray(indices)

        # `indices` is 2D: each row is a permutation of the indices.
        # We use it to index `data` along its last axis, which corresponds
        # with observations.
        # After indexing, the second to last axis of `data_batch` corresponds
        # with permutations, and the last axis corresponds with observations.
        # data_batch = data[..., indices]
        data_batch = _get_from_last_axis(data, indices, xp=xp)

        # Move the permutation axis to the front: we'll concatenate a list
        # of batched statistic values along this zeroth axis to form the
        # null distribution.
        data_batch = xp.moveaxis(data_batch, -2, 0)
        # data_batch = np.split(data_batch, n_obs_ic[:-1], axis=-1)
        data_batch = [data_batch[..., i:j] for i, j in zip(n_obs_ic[:-1], n_obs_ic[1:])]
        null_distribution.append(statistic(*data_batch, axis=-1))
    null_distribution = xp.concat(null_distribution, axis=0)

    return null_distribution, n_permutations, exact_test

