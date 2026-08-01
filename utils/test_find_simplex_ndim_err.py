
def test_find_simplex_ndim_err():
    generators = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
    tri = qhull.Delaunay(generators)
    with pytest.raises(ValueError):
        tri.find_simplex([2, 2, 2])

