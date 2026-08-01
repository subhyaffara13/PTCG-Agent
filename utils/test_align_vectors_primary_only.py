
def test_align_vectors_primary_only(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-12 if dtype == xp.float64 else 1e-5
    mats_a = Rotation.random(100, rng=0).as_matrix()
    mats_b = Rotation.random(100, rng=1).as_matrix()

    for mat_a, mat_b in zip(mats_a, mats_b):
        # Get random 3-element unit vectors
        a = xp.asarray(mat_a[0], dtype=dtype)
        b = xp.asarray(mat_b[0], dtype=dtype)

        # Compare to align_vectors with primary only
        R, rssd = Rotation.align_vectors(a, b)
        xp_assert_close(R.apply(b), a, atol=atol)
        xp_assert_close(rssd, xp.asarray(0.0)[()], atol=atol)

