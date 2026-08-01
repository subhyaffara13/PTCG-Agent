
def test_contains_point():
    ell = mpatches.Ellipse((0.5, 0.5), 0.5, 1.0)
    points = [(0.0, 0.5), (0.2, 0.5), (0.25, 0.5), (0.5, 0.5)]
    path = ell.get_path()
    transform = ell.get_transform()
    radius = ell._process_radius(None)
    expected = np.array([path.contains_point(point,
                                             transform,
                                             radius) for point in points])
    result = np.array([ell.contains_point(point) for point in points])
    assert np.all(result == expected)

