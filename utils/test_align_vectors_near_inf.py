
def test_align_vectors_near_inf(xp):
    # align_vectors should return near the same result for high weights as for
    # infinite weights. rssd will be different with floating point error on the
    # exactly aligned vector being multiplied by a large non-infinite weight
    dtype = xpx.default_dtype(xp)
    if dtype == xp.float32:
        pytest.skip("Align vectors near inf is numerically unstable in float32")
    n = 100
    mats = []
    for i in range(6):
        mats.append(Rotation.random(n, rng=10 + i).as_matrix())

    for i in range(n):
        # Get random pairs of 3-element vectors
        a = xp.asarray(np.array([1 * mats[0][i][0], 2 * mats[1][i][0]]), dtype=dtype)
        b = xp.asarray(np.array([3 * mats[2][i][0], 4 * mats[3][i][0]]), dtype=dtype)

        R, _ = Rotation.align_vectors(a, b, weights=[1e10, 1])
        R2, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 1])
        xp_assert_close(R.as_matrix(), R2.as_matrix(), atol=1e-4)

    for i in range(n):
        # Get random triplets of 3-element vectors
        a = xp.asarray(np.array([1*mats[0][i][0], 2*mats[1][i][0], 3*mats[2][i][0]]),
                       dtype=dtype)
        b = xp.asarray(np.array([4*mats[3][i][0], 5*mats[4][i][0], 6*mats[5][i][0]]),
                       dtype=dtype)

        R, _ = Rotation.align_vectors(a, b, weights=[1e10, 2, 1])
        R2, _ = Rotation.align_vectors(a, b, weights=[xp.inf, 2, 1])
        xp_assert_close(R.as_matrix(), R2.as_matrix(), atol=1e-4)

