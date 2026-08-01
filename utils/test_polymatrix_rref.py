
def test_polymatrix_rref():
    M = PolyMatrix([[1, 2], [3, 4]], x)
    assert M.rref() == (PolyMatrix.eye(2, x), (0, 1))
    raises(ValueError, lambda: PolyMatrix([1, 2], ring=ZZ[x]).rref())
    raises(ValueError, lambda: PolyMatrix([1, x], ring=QQ[x]).rref())

