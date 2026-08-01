
def test_delaunay_insufficient_points(x, y):
    with pytest.raises(ValueError):
        mtri.Triangulation(x, y)

