
def test_tricontourf_path():
    x = [0, 4, 4, 0, 2]
    y = [0, 0, 4, 4, 2]
    triang = mtri.Triangulation(x, y)
    _, ax = plt.subplots()

    # Polygon inside domain
    cs = ax.tricontourf(triang, [0, 0, 0, 0, 1], levels=[0.5, 1.5])
    paths = cs.get_paths()
    assert len(paths) == 1
    expected_vertices = [[3, 1], [3, 3], [1, 3], [1, 1], [3, 1]]
    assert_array_almost_equal(paths[0].vertices, expected_vertices)
    assert_array_equal(paths[0].codes, [1, 2, 2, 2, 79])
    assert_array_almost_equal(paths[0].to_polygons(), [expected_vertices])

    # Polygon following boundary and inside domain
    cs = ax.tricontourf(triang, [1, 0, 0, 0, 0], levels=[0.5, 1.5])
    paths = cs.get_paths()
    assert len(paths) == 1
    expected_vertices = [[2, 0], [1, 1], [0, 2], [0, 0], [2, 0]]
    assert_array_almost_equal(paths[0].vertices, expected_vertices)
    assert_array_equal(paths[0].codes, [1, 2, 2, 2, 79])
    assert_array_almost_equal(paths[0].to_polygons(), [expected_vertices])

    # Polygon is outer boundary with hole
    cs = ax.tricontourf(triang, [0, 0, 0, 0, 1], levels=[-0.5, 0.5])
    paths = cs.get_paths()
    assert len(paths) == 1
    expected_vertices = [[0, 0], [4, 0], [4, 4], [0, 4], [0, 0],
                         [1, 1], [1, 3], [3, 3], [3, 1], [1, 1]]
    assert_array_almost_equal(paths[0].vertices, expected_vertices)
    assert_array_equal(paths[0].codes, [1, 2, 2, 2, 79, 1, 2, 2, 2, 79])
    assert_array_almost_equal(paths[0].to_polygons(), np.split(expected_vertices, [5]))

