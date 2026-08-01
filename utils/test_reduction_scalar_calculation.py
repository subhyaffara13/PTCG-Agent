
def test_reduction_scalar_calculation(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-6
    rng = np.random.default_rng(146972845698875399755764481408308808739)
    l_np = Rotation.random(5, rng=rng)
    r_np = Rotation.random(10, rng=rng)
    p_np = Rotation.random(7, rng=rng)
    l = rotation_to_xp(l_np, xp)
    r = rotation_to_xp(r_np, xp)
    p = rotation_to_xp(p_np, xp)
    reduced, left_best, right_best = p.reduce(l, r, return_indices=True)

    # Loop implementation of the vectorized calculation in Rotation.reduce
    scalars = np.zeros((len(l_np), len(p_np), len(r_np)))
    for i, li in enumerate(l_np):
        for j, pj in enumerate(p_np):
            for k, rk in enumerate(r_np):
                scalars[i, j, k] = np.abs((li * pj * rk).as_quat()[3])
    scalars = np.reshape(np.moveaxis(scalars, 1, 0), (scalars.shape[1], -1))

    max_ind = np.argmax(np.reshape(scalars, (len(p), -1)), axis=1)
    left_best_check = xp.asarray(max_ind // len(r))
    right_best_check = xp.asarray(max_ind % len(r))
    assert xp.all(left_best == left_best_check)
    assert xp.all(right_best == right_best_check)

    reduced_check = l[left_best_check] * p * r[right_best_check]
    mag = (reduced.inv() * reduced_check).magnitude()
    xp_assert_close(mag, xp.zeros(len(p)), atol=atol)

