
def test_negative_real_gh14582(derivative, fun):
    # gh-14582 reported that the spherical Bessel functions did not work
    # with negative real argument `z`. Check that this is resolved.
    rng = np.random.default_rng(3598435982345987234)
    size = 25
    n = rng.integers(0, 10, size=size)
    z = rng.standard_normal(size=size)
    res = fun(n, z, derivative=derivative)
    ref = fun(n, z+0j, derivative=derivative)
    assert_allclose(res, ref.real)

