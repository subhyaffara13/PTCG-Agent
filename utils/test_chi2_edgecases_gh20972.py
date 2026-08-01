
def test_chi2_edgecases_gh20972():
    # Tests that a variety of edgecases for chi square distribution functions
    # correctly return NaN when and only when they are supposed to, when
    # computed through different related ufuncs. See gh-20972.
    v = np.asarray([-0.01, 0, 0.01, 1, np.inf])[:, np.newaxis]
    x = np.asarray([-np.inf, -0.01, 0, 0.01, np.inf])

    # Check that `gammainc` is NaN when it should be and finite otherwise
    ref = special.gammainc(v / 2, x / 2)
    mask = (x < 0) | (v < 0) | (x == 0) & (v == 0) | np.isinf(v) & np.isinf(x)
    assert np.all(np.isnan(ref[mask]))
    assert np.all(np.isfinite(ref[~mask]))

    # Use `gammainc` as a reference for the rest
    assert_allclose(special.chdtr(v, x), ref)
    assert_allclose(special.gdtr(1, v / 2, x / 2), ref)
    assert_allclose(1 - special.gammaincc(v / 2, x / 2), ref)
    assert_allclose(1 - special.chdtrc(v, x), ref)
    assert_allclose(1 - special.gdtrc(1, v / 2, x / 2), ref)

