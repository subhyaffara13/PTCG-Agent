from pathlib import Path


def test_interpolated_moveto():
    # Initial path has two subpaths with two LINETOs each
    vertices = np.array([[0, 0],
                         [0, 1],
                         [1, 2],
                         [4, 4],
                         [4, 5],
                         [5, 5]])
    codes = [Path.MOVETO, Path.LINETO, Path.LINETO] * 2

    path = Path(vertices, codes)
    result = path.interpolated(3)

    # Result should have two subpaths with six LINETOs each
    expected_subpath_codes = [Path.MOVETO] + [Path.LINETO] * 6
    np.testing.assert_array_equal(result.codes, expected_subpath_codes * 2)

