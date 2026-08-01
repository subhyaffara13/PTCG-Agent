
def _mixed_data_generator(n_samples, n_repetitions, axis, rng,
                          paired=False):
    # generate random samples to check the response of hypothesis tests to
    # samples with different (but broadcastable) shapes and various
    # nan patterns (e.g. all nans, some nans, no nans) along axis-slices

    data = []
    for i in range(n_samples):
        n_patterns = 6  # number of distinct nan patterns
        n_obs = 20 if paired else 20 + i  # observations per axis-slice
        x = np.ones((n_repetitions, n_patterns, n_obs)) * np.nan

        for j in range(n_repetitions):
            samples = x[j, :, :]

            # case 0: axis-slice with all nans (0 reals)
            # cases 1-3: axis-slice with 1-3 reals (the rest nans)
            # case 4: axis-slice with mostly (all but two) reals
            # case 5: axis slice with all reals
            for k, n_reals in enumerate([0, 1, 2, 3, n_obs-2, n_obs]):
                # for cases 1-3, need paired nansw  to be in the same place
                indices = rng.permutation(n_obs)[:n_reals]
                samples[k, indices] = rng.random(size=n_reals)

            # permute the axis-slices just to show that order doesn't matter
            samples[:] = rng.permutation(samples, axis=0)

        # For multi-sample tests, we want to test broadcasting and check
        # that nan policy works correctly for each nan pattern for each input.
        # This takes care of both simultaneously.
        new_shape = [n_repetitions] + [1]*n_samples + [n_obs]
        new_shape[1 + i] = 6
        x = x.reshape(new_shape)

        x = np.moveaxis(x, -1, axis)
        data.append(x)
    return data

