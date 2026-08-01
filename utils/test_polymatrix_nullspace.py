
def test_polymatrix_nullspace():
    M = PolyMatrix([[1, 2], [3, 6]], x)
    assert M.nullspace() == [PolyMatrix([-2, 1], x)]
    raises(ValueError, lambda: PolyMatrix([1, 2], ring=ZZ[x]).nullspace())
    raises(ValueError, lambda: PolyMatrix([1, x], ring=QQ[x]).nullspace())
    assert M.rank() == 1

