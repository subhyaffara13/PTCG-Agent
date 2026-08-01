
def test_Normalize():
    norm = mcolors.Normalize()
    vals = np.arange(-10, 10, 1, dtype=float)
    _inverse_tester(norm, vals)
    _scalar_tester(norm, vals)
    _mask_tester(norm, vals)

    # Handle integer input correctly (don't overflow when computing max-min,
    # i.e. 127-(-128) here).
    vals = np.array([-128, 127], dtype=np.int8)
    norm = mcolors.Normalize(vals.min(), vals.max())
    assert_array_equal(norm(vals), [0, 1])

    # Don't lose precision on longdoubles (float128 on Linux):
    # for array inputs...
    vals = np.array([1.2345678901, 9.8765432109], dtype=np.longdouble)
    norm = mcolors.Normalize(vals[0], vals[1])
    assert norm(vals).dtype == np.longdouble
    assert_array_equal(norm(vals), [0, 1])
    # and for scalar ones.
    eps = np.finfo(np.longdouble).resolution
    norm = plt.Normalize(1, 1 + 100 * eps)
    # This returns exactly 0.5 when longdouble is extended precision (80-bit),
    # but only a value close to it when it is quadruple precision (128-bit).
    assert_array_almost_equal(norm(1 + 50 * eps), 0.5, decimal=3)

