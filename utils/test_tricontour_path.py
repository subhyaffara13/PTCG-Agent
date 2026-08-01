
def test_tricontour_path():
    x = [0, 4, 4, 0, 2]
    y = [0, 0, 4, 4, 2]
    triang = mtri.Triangulation(x, y)
    _, ax = plt.subplots()

    # Line strip from boundary to boundary
    cs = ax.tricontour(triang, [1, 0, 0, 0, 0], levels=[0.5])
    paths = cs.get_paths()
    assert len(paths) == 1
    expected_vertices = [[2, 0], [1, 1], [0, 2]]
    assert_array_almost_equal(paths[0].vertices, expected_vertices)
    assert_array_equal(paths[0].codes, [1, 2, 2])
    assert_array_almost_equal(
        paths[0].to_polygons(closed_only=False), [expected_vertices])

    # Closed line loop inside domain
    cs = ax.tricontour(triang, [0, 0, 0, 0, 1], levels=[0.5])
    paths = cs.get_paths()
    assert len(paths) == 1
    expected_vertices = [[3, 1], [3, 3], [1, 3], [1, 1], [3, 1]]
    assert_array_almost_equal(paths[0].vertices, expected_vertices)
    assert_array_equal(paths[0].codes, [1, 2, 2, 2, 79])
    assert_array_almost_equal(paths[0].to_polygons(), [expected_vertices])

