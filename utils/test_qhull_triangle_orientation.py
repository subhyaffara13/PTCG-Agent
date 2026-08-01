
def test_qhull_triangle_orientation():
    # github issue 4437.
    xi = np.linspace(-2, 2, 100)
    x, y = map(np.ravel, np.meshgrid(xi, xi))
    w = (x > y - 1) & (x < -1.95) & (y > -1.2)
    x, y = x[w], y[w]
    theta = np.radians(25)
    x1 = x*np.cos(theta) - y*np.sin(theta)
    y1 = x*np.sin(theta) + y*np.cos(theta)

    # Calculate Delaunay triangulation using Qhull.
    triang = mtri.Triangulation(x1, y1)

    # Neighbors returned by Qhull.
    qhull_neighbors = triang.neighbors

    # Obtain neighbors using own C++ calculation.
    triang._neighbors = None
    own_neighbors = triang.neighbors

    assert_array_equal(qhull_neighbors, own_neighbors)

