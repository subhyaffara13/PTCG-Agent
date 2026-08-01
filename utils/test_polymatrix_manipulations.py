
def test_polymatrix_manipulations():
    M1 = PolyMatrix([[1, 2], [3, 4]], x)
    assert M1.transpose() == PolyMatrix([[1, 3], [2, 4]], x)
    M2 = PolyMatrix([[5, 6], [7, 8]], x)
    assert M1.row_join(M2) == PolyMatrix([[1, 2, 5, 6], [3, 4, 7, 8]], x)
    assert M1.col_join(M2) == PolyMatrix([[1, 2], [3, 4], [5, 6], [7, 8]], x)
    assert M1.applyfunc(lambda e: 2*e) == PolyMatrix([[2, 4], [6, 8]], x)

