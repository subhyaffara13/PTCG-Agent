
def test_contains_points():
    ell = mpatches.Ellipse((0.5, 0.5), 0.5, 1.0)
    points = [(0.0, 0.5), (0.2, 0.5), (0.25, 0.5), (0.5, 0.5)]
    path = ell.get_path()
    transform = ell.get_transform()
    radius = ell._process_radius(None)
    expected = path.contains_points(points, transform, radius)
    result = ell.contains_points(points)
    assert np.all(result == expected)

