
def test_delaunay():
    # No duplicate points, regular grid.
    nx = 5
    ny = 4
    x, y = np.meshgrid(np.linspace(0.0, 1.0, nx), np.linspace(0.0, 1.0, ny))
    x = x.ravel()
    y = y.ravel()
    npoints = nx*ny
    ntriangles = 2 * (nx-1) * (ny-1)
    nedges = 3*nx*ny - 2*nx - 2*ny + 1

    # Create delaunay triangulation.
    triang = mtri.Triangulation(x, y)

    # The tests in the remainder of this function should be passed by any
    # triangulation that does not contain duplicate points.

    # Points - floating point.
    assert_array_almost_equal(triang.x, x)
    assert_array_almost_equal(triang.y, y)

    # Triangles - integers.
    assert len(triang.triangles) == ntriangles
    assert np.min(triang.triangles) == 0
    assert np.max(triang.triangles) == npoints-1

    # Edges - integers.
    assert len(triang.edges) == nedges
    assert np.min(triang.edges) == 0
    assert np.max(triang.edges) == npoints-1

    # Neighbors - integers.
    # Check that neighbors calculated by C++ triangulation class are the same
    # as those returned from delaunay routine.
    neighbors = triang.neighbors
    triang._neighbors = None
    assert_array_equal(triang.neighbors, neighbors)

    # Is each point used in at least one triangle?
    assert_array_equal(np.unique(triang.triangles), np.arange(npoints))

