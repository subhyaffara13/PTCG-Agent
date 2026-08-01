
def test_gh_21286():
    generators = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
    tri = qhull.Delaunay(generators)
    # verify absence of segfault reported in ticket:
    with pytest.raises(IndexError):
        tri.find_simplex(1)
    with pytest.raises(IndexError):
        # strikingly, Delaunay object has shape
        # () just like np.asanyarray(1) above
        tri.find_simplex(tri)

