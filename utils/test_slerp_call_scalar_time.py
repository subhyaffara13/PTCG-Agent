
def test_slerp_call_scalar_time(xp):
    dtype = xpx.default_dtype(xp)
    atol = 1e-16 if dtype == xp.float64 else 1e-7
    r = Rotation.from_euler('X', xp.asarray([[0], [80]]), degrees=True)
    s = Slerp([0, 1], r)

    r_interpolated = s(0.25)
    r_interpolated_expected = Rotation.from_euler('X', xp.asarray(20), degrees=True)

    delta = r_interpolated * r_interpolated_expected.inv()

    xp_assert_close(delta.magnitude(), xp.asarray(0.0)[()], atol=atol)

