
def test_nanfunctions_matrices_general():
    # Check that it works and that type and
    # shape are preserved
    # 2018-04-29: moved here from core.tests.test_nanfunctions
    mat = np.matrix(np.eye(3))
    for f in (np.nanargmin, np.nanargmax, np.nansum, np.nanprod,
              np.nanmean, np.nanvar, np.nanstd):
        res = f(mat, axis=0)
        assert_(isinstance(res, np.matrix))
        assert_(res.shape == (1, 3))
        res = f(mat, axis=1)
        assert_(isinstance(res, np.matrix))
        assert_(res.shape == (3, 1))
        res = f(mat)
        assert_(np.isscalar(res))

    for f in np.nancumsum, np.nancumprod:
        res = f(mat, axis=0)
        assert_(isinstance(res, np.matrix))
        assert_(res.shape == (3, 3))
        res = f(mat, axis=1)
        assert_(isinstance(res, np.matrix))
        assert_(res.shape == (3, 3))
        res = f(mat)
        assert_(isinstance(res, np.matrix))
        assert_(res.shape == (1, 3 * 3))

