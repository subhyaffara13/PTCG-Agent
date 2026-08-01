
def test_error_handling():
    with pytest.raises(ValueError):
        RotationSpline([1.0], Rotation.random())

    r = Rotation.random(10)
    t = np.arange(10).reshape(5, 2)
    with pytest.raises(ValueError):
        RotationSpline(t, r)

    t = np.arange(9)
    with pytest.raises(ValueError):
        RotationSpline(t, r)

    t = np.arange(10)
    t[5] = 0
    with pytest.raises(ValueError):
        RotationSpline(t, r)

    t = np.arange(10)

    s = RotationSpline(t, r)
    with pytest.raises(ValueError):
        s(10, -1)

    with pytest.raises(ValueError):
        s(np.arange(10).reshape(5, 2))

    r = Rotation.from_quat(np.array([[[0.0, 0, 0, 1], [1, 0, 0 ,0]]]))
    t = np.arange(2)
    with pytest.raises(ValueError):
        RotationSpline(t, r)  # More than 2 dimensions

