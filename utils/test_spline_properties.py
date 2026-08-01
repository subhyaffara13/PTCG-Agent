
def test_spline_properties():
    times = np.array([0, 5, 15, 27])
    angles = [[-5, 10, 27], [3, 5, 38], [-12, 10, 25], [-15, 20, 11]]

    rotations = Rotation.from_euler('xyz', angles, degrees=True)
    spline = RotationSpline(times, rotations)

    assert_allclose(spline(times).as_euler('xyz', degrees=True), angles)
    assert_allclose(spline(0).as_euler('xyz', degrees=True), angles[0])

    h = 1e-8
    rv0 = spline(times).as_rotvec()
    rvm = spline(times - h).as_rotvec()
    rvp = spline(times + h).as_rotvec()
    # rtol bumped from 1e-15 to 1.5e-15 in gh18414 for linux 32 bit
    assert_allclose(rv0, 0.5 * (rvp + rvm), rtol=1.5e-15)

    r0 = spline(times, 1)
    rm = spline(times - h, 1)
    rp = spline(times + h, 1)
    assert_allclose(r0, 0.5 * (rm + rp), rtol=1e-14)

    a0 = spline(times, 2)
    am = spline(times - h, 2)
    ap = spline(times + h, 2)
    assert_allclose(a0, am, rtol=1e-7)
    assert_allclose(a0, ap, rtol=1e-7)

