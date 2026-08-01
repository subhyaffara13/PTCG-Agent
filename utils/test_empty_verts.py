
def test_empty_verts():
    poly = Polygon(np.zeros((0, 2)))
    assert poly.get_verts() == []

