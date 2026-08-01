
def test_spline_2_rotations():
    times = [0, 10]
    rotations = Rotation.from_euler('xyz', [[0, 0, 0], [10, -20, 30]],
                                    degrees=True)
    spline = RotationSpline(times, rotations)

    rv = (rotations[0].inv() * rotations[1]).as_rotvec()
    rate = rv / (times[1] - times[0])
    times_check = np.array([-1, 5, 12])
    dt = times_check - times[0]
    rv_ref = rate * dt[:, None]

    assert_allclose(spline(times_check).as_rotvec(), rv_ref)
    assert_allclose(spline(times_check, 1), np.resize(rate, (3, 3)))
    assert_allclose(spline(times_check, 2), 0, atol=1e-16)

