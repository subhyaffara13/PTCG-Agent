
def _homogeneous_data_generator(n_samples, n_repetitions, axis, rng,
                                paired=False, all_nans=True):
    # generate random samples to check the response of hypothesis tests to
    # samples with different (but broadcastable) shapes and homogeneous
    # data (all nans or all finite)
    data = []
    for i in range(n_samples):
        n_obs = 20 if paired else 20 + i  # observations per axis-slice
        shape = [n_repetitions] + [1]*n_samples + [n_obs]
        shape[1 + i] = 2
        x = np.ones(shape) * np.nan if all_nans else rng.random(shape)
        x = np.moveaxis(x, -1, axis)
        data.append(x)
    return data

