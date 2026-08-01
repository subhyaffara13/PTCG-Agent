
def test_polymatrix_from_Matrix():
    assert PolyMatrix.from_Matrix(Matrix([1, 2]), x) == PolyMatrix([1, 2], x, ring=QQ[x])
    assert PolyMatrix.from_Matrix(Matrix([1]), ring=QQ[x]) == PolyMatrix([1], x)
    pmx = PolyMatrix([1, 2], x)
    pmy = PolyMatrix([1, 2], y)
    assert pmx != pmy
    assert pmx.set_gens(y) == pmy

