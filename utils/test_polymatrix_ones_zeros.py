
def test_polymatrix_ones_zeros():
    assert PolyMatrix.zeros(1, 2, x) == PolyMatrix([[0, 0]], x)
    assert PolyMatrix.eye(2, x) == PolyMatrix([[1, 0], [0, 1]], x)

