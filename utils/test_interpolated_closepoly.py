from pathlib import Path


def test_interpolated_closepoly():
    codes = [Path.MOVETO] + [Path.LINETO]*2 + [Path.CLOSEPOLY]
    vertices = [(4, 3), (5, 4), (5, 3), (0, 0)]

    path = Path(vertices, codes)
    result = path.interpolated(2)

    expected_vertices = np.array([[4, 3],
                                  [4.5, 3.5],
                                  [5, 4],
                                  [5, 3.5],
                                  [5, 3],
                                  [4.5, 3],
                                  [4, 3]])
    expected_codes = [Path.MOVETO] + [Path.LINETO]*5 + [Path.CLOSEPOLY]

    np.testing.assert_allclose(result.vertices, expected_vertices)
    np.testing.assert_array_equal(result.codes, expected_codes)

    # Usually closepoly is the last vertex but does not have to be.
    codes += [Path.LINETO]
    vertices += [(2, 1)]

    path = Path(vertices, codes)
    result = path.interpolated(2)

    extra_expected_vertices = np.array([[3, 2],
                                        [2, 1]])
    expected_vertices = np.concatenate([expected_vertices, extra_expected_vertices])

    expected_codes += [Path.LINETO] * 2

    np.testing.assert_allclose(result.vertices, expected_vertices)
    np.testing.assert_array_equal(result.codes, expected_codes)

