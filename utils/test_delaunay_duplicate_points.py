
def test_delaunay_duplicate_points():
    npoints = 10
    duplicate = 7
    duplicate_of = 3

    np.random.seed(23)
    x = np.random.random(npoints)
    y = np.random.random(npoints)
    x[duplicate] = x[duplicate_of]
    y[duplicate] = y[duplicate_of]

    # Create delaunay triangulation.
    triang = mtri.Triangulation(x, y)

    # Duplicate points should be ignored, so the index of the duplicate points
    # should not appear in any triangle.
    assert_array_equal(np.unique(triang.triangles),
                       np.delete(np.arange(npoints), duplicate))

