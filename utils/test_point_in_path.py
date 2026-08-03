from pathlib import Path


def test_point_in_path():
    # Test #1787
    path = Path._create_closed([(0, 0), (0, 1), (1, 1), (1, 0)])
    points = [(0.5, 0.5), (1.5, 0.5)]
    ret = path.contains_points(points)
    assert ret.dtype == 'bool'
    np.testing.assert_equal(ret, [True, False])

