
def test_lambertw_ufunc_loop_selection():
    # see https://github.com/scipy/scipy/issues/4895
    dt = np.dtype(np.complex128)
    assert_equal(lambertw(0, 0, 0).dtype, dt)
    assert_equal(lambertw([0], 0, 0).dtype, dt)
    assert_equal(lambertw(0, [0], 0).dtype, dt)
    assert_equal(lambertw(0, 0, [0]).dtype, dt)
    assert_equal(lambertw([0], [0], [0]).dtype, dt)

