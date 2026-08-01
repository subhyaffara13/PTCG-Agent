
def _pairings_permutations_gen(n_permutations, n_samples, n_obs_sample, batch,
                               rng):
    # Returns a generator that yields arrays of size
    # `(batch, n_samples, n_obs_sample)`.
    # Each row is an independent permutation of indices 0 to `n_obs_sample`.
    batch = min(batch, n_permutations)

    if hasattr(rng, 'permuted'):
        def batched_perm_generator():
            indices = np.arange(n_obs_sample)
            indices = np.tile(indices, (batch, n_samples, 1))
            for k in range(0, n_permutations, batch):
                batch_actual = min(batch, n_permutations-k)
                # Don't permute in place, otherwise results depend on `batch`
                permuted_indices = rng.permuted(indices, axis=-1)
                yield permuted_indices[:batch_actual]
    else:  # RandomState and early Generators don't have `permuted`
        def batched_perm_generator():
            for k in range(0, n_permutations, batch):
                batch_actual = min(batch, n_permutations-k)
                size = (batch_actual, n_samples, n_obs_sample)
                x = rng.random(size=size)
                yield np.argsort(x, axis=-1)[:batch_actual]

    return batched_perm_generator()

