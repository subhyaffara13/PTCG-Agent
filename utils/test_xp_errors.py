
def test_xp_errors(xp):
    times = xp.asarray([0, 10])
    r = Rotation.random(2)
    r = Rotation.from_quat(xp.asarray(r.as_quat()))
    s = RotationSpline(times, r)
    t = xp.asarray([0.5, 1.5])
    # RotationSpline does not have native Array API support, so we check that it
    # converts any array to NumPy and outputs NumPy arrays.
    assert isinstance(s(t).as_quat(), np.ndarray)

