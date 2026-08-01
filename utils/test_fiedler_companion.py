
def test_fiedler_companion():
    fc = fiedler_companion([])
    assert_equal(fc.size, 0)
    fc = fiedler_companion([1.])
    assert_equal(fc.size, 0)
    assert_equal(fc.shape, (0, 0))
    fc = fiedler_companion([1., 2.])
    assert_array_equal(fc, np.array([[-2.]]))
    fc = fiedler_companion([1e-12, 2., 3.])
    assert_array_almost_equal(fc, companion([1e-12, 2., 3.]))
    with assert_raises(ValueError):
        fiedler_companion([0, 1, 2])
    fc = fiedler_companion([1., -16., 86., -176., 105.])
    assert_array_almost_equal(eigvals(fc),
                              np.array([7., 5., 3., 1.]))

