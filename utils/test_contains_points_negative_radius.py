from pathlib import Path


def test_contains_points_negative_radius():
    path = Path.unit_circle()

    points = [(0.0, 0.0), (1.25, 0.0), (0.9, 0.9)]
    result = path.contains_points(points, radius=-0.5)
    np.testing.assert_equal(result, [True, False, False])

