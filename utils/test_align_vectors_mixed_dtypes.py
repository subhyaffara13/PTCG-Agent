
def test_align_vectors_mixed_dtypes(xp):
    dtype = xpx.default_dtype(xp)
    rng = np.random.default_rng(123)
    c = rotation_to_xp(Rotation.random(rng=rng), xp)
    b = xp.asarray(rng.normal(size=(5, 3)), dtype=dtype)
    a = xp.asarray(c.apply(b), dtype=xp.float32)  # Intentionally float32
    # Check that the dtype of the output is the result type of a and b
    est, _ = Rotation.align_vectors(a, b)
    xp_assert_close(est.as_quat(), c.as_quat())

