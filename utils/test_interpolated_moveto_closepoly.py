
def test_interpolated_moveto_closepoly():
    # Initial path has two closed subpaths
    codes = ([Path.MOVETO] + [Path.LINETO]*2 + [Path.CLOSEPOLY]) * 2
    vertices = [(4, 3), (5, 4), (5, 3), (0, 0), (8, 6), (10, 8), (10, 6), (0, 0)]

    path = Path(vertices, codes)
    result = path.interpolated(2)

    expected_vertices1 = np.array([[4, 3],
                                   [4.5, 3.5],
                                   [5, 4],
                                   [5, 3.5],
                                   [5, 3],
                                   [4.5, 3],
                                   [4, 3]])
    expected_vertices = np.concatenate([expected_vertices1, expected_vertices1 * 2])
    expected_codes = ([Path.MOVETO] + [Path.LINETO]*5 + [Path.CLOSEPOLY]) * 2

    np.testing.assert_allclose(result.vertices, expected_vertices)
    np.testing.assert_array_equal(result.codes, expected_codes)

