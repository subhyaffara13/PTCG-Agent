
def test_all_points_on_plane():
    # Non-coplanar points
    points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert not _all_points_on_plane(*points.T)

    # Duplicate points
    points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]])
    assert _all_points_on_plane(*points.T)

    # NaN values
    points = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, np.nan]])
    assert _all_points_on_plane(*points.T)

    # Less than 3 unique points
    points = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert _all_points_on_plane(*points.T)

    # All points lie on a line
    points = np.array([[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 3, 0]])
    assert _all_points_on_plane(*points.T)

    # All points lie on two lines, with antiparallel vectors
    points = np.array([[-2, 2, 0], [-1, 1, 0], [1, -1, 0],
                       [0, 0, 0], [2, 0, 0], [1, 0, 0]])
    assert _all_points_on_plane(*points.T)

    # All points lie on a plane
    points = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [1, 2, 0]])
    assert _all_points_on_plane(*points.T)

