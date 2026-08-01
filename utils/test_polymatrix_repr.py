
def test_polymatrix_repr():
    assert repr(PolyMatrix([[1, 2]], x)) == 'PolyMatrix([[1, 2]], ring=QQ[x])'
    assert repr(PolyMatrix(0, 2, [], x)) == 'PolyMatrix(0, 2, [], ring=QQ[x])'

