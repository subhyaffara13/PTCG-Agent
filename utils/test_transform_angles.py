
def test_transform_angles():
    t = mtransforms.Affine2D()  # Identity transform
    angles = np.array([20, 45, 60])
    points = np.array([[0, 0], [1, 1], [2, 2]])

    # Identity transform does not change angles
    new_angles = t.transform_angles(angles, points)
    assert_array_almost_equal(angles, new_angles)

    # points missing a 2nd dimension
    with pytest.raises(ValueError):
        t.transform_angles(angles, points[0:2, 0:1])

    # Number of angles != Number of points
    with pytest.raises(ValueError):
        t.transform_angles(angles, points[0:2, :])

