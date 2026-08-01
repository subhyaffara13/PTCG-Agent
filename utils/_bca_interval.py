
def _bca_interval(data, statistic, axis, alpha, theta_hat_b, batch, xp):
    """Bias-corrected and accelerated interval."""
    # closely follows [1] 14.3 and 15.4 (Eq. 15.36)

    # calculate z0_hat
    theta_hat = xp.expand_dims(statistic(*data, axis=axis), axis=-1)
    percentile = _percentile_of_score(theta_hat_b, theta_hat, axis=-1, xp=xp)
    percentile = xp.asarray(percentile, dtype=theta_hat.dtype,
                            device=xp_device(theta_hat))
    z0_hat = ndtri(percentile)

    # calculate a_hat
    theta_hat_ji = []  # j is for sample of data, i is for jackknife resample
    for j, sample in enumerate(data):
        # _jackknife_resample will add an axis prior to the last axis that
        # corresponds with the different jackknife resamples. Do the same for
        # each sample of the data to ensure broadcastability. We need to
        # create a copy of the list containing the samples anyway, so do this
        # in the loop to simplify the code. This is not the bottleneck...
        samples = [xp.expand_dims(sample, axis=-2) for sample in data]
        theta_hat_i = []
        for jackknife_sample in _jackknife_resample(sample, batch, xp=xp):
            samples[j] = jackknife_sample
            broadcasted = _broadcast_arrays(samples, axis=-1, xp=xp)
            theta_hat_i.append(statistic(*broadcasted, axis=-1))
        theta_hat_ji.append(theta_hat_i)

    theta_hat_ji = [xp.concat(theta_hat_i, axis=-1)
                    for theta_hat_i in theta_hat_ji]

    # CuPy array dtype is unstable in 1.13.6 when divided by large Python int:
    # (cp.ones(1, dtype=cp.float32)/10000).dtype   # float32
    # (cp.ones(1, dtype=cp.float32)/100000).dtype  # float64
    # Solution for now is to make the divisor a Python float
    # Looks like this will be fixed in 1.14.0
    n_j = [float(theta_hat_i.shape[-1]) for theta_hat_i in theta_hat_ji]

    theta_hat_j_dot = [xp.mean(theta_hat_i, axis=-1, keepdims=True)
                       for theta_hat_i in theta_hat_ji]

    U_ji = [(n - 1) * (theta_hat_dot - theta_hat_i)
            for theta_hat_dot, theta_hat_i, n
            in zip(theta_hat_j_dot, theta_hat_ji, n_j)]

    nums = [xp.sum(U_i**3, axis=-1)/n**3 for U_i, n in zip(U_ji, n_j)]
    dens = [xp.sum(U_i**2, axis=-1)/n**2 for U_i, n in zip(U_ji, n_j)]
    a_hat = 1/6 * sum(nums) / sum(dens)**(3/2)

    # calculate alpha_1, alpha_2
    # `float` because dtype of ndtri output (float64) should not promote other vals
    z_alpha = float(ndtri(alpha))
    z_1alpha = -z_alpha
    num1 = z0_hat + z_alpha
    alpha_1 = ndtr(z0_hat + num1/(1 - a_hat*num1))
    num2 = z0_hat + z_1alpha
    alpha_2 = ndtr(z0_hat + num2/(1 - a_hat*num2))
    return alpha_1, alpha_2, a_hat  # return a_hat for testing

