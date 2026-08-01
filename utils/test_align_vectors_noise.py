
def test_align_vectors_noise(xp):
    dtype = xpx.default_dtype(xp)
    rng = np.random.default_rng(146972845698875399755764481408308808739)
    n_vectors = 100
    rot = rotation_to_xp(Rotation.random(rng=rng), xp)
    vectors = xp.asarray(rng.normal(size=(n_vectors, 3)), dtype=dtype)
    result = rot.apply(vectors)

    # The paper adds noise as independently distributed angular errors
    sigma = np.deg2rad(1)
    tolerance = 1.5 * sigma
    noise = Rotation.from_rotvec(
        xp.asarray(rng.normal(size=(n_vectors, 3), scale=sigma), dtype=dtype)
    )

    # Attitude errors must preserve norm. Hence apply individual random
    # rotations to each vector.
    noisy_result = noise.apply(result)

    est, rssd, cov = Rotation.align_vectors(noisy_result, vectors,
                                            return_sensitivity=True)

    # Use rotation compositions to find out closeness
    error_vector = (rot * est.inv()).as_rotvec()
    xp_assert_close(error_vector[0], xp.asarray(0.0)[()], atol=tolerance)
    xp_assert_close(error_vector[1], xp.asarray(0.0)[()], atol=tolerance)
    xp_assert_close(error_vector[2], xp.asarray(0.0)[()], atol=tolerance)

    # Check error bounds using covariance matrix
    cov *= xp.asarray(sigma)
    xp_assert_close(cov[0, 0], xp.asarray(0.0)[()], atol=tolerance)
    xp_assert_close(cov[1, 1], xp.asarray(0.0)[()], atol=tolerance)
    xp_assert_close(cov[2, 2], xp.asarray(0.0)[()], atol=tolerance)

    rssd_check = xp.sum((noisy_result - est.apply(vectors)) ** 2) ** 0.5
    xp_assert_close(rssd, rssd_check, check_shape=False)

