
def test_group_var_large_inputs():
    dtype = np.float64
    prng = np.random.default_rng(2)

    out = np.array([[np.nan]], dtype=dtype)
    counts = np.array([0], dtype="int64")
    values = (prng.random((10**6, 1)) + 10**12).astype(dtype)
    labels = np.zeros(10**6, dtype="intp")

    group_var(out, counts, values, labels)

    assert counts[0] == 10**6
    tm.assert_almost_equal(out[0, 0], 1.0 / 12, rtol=0.5e-3)

