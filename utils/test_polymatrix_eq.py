
def test_polymatrix_eq():
    assert (PolyMatrix([x]) == PolyMatrix([x])) is True
    assert (PolyMatrix([y]) == PolyMatrix([x])) is False
    assert (PolyMatrix([x]) != PolyMatrix([x])) is False
    assert (PolyMatrix([y]) != PolyMatrix([x])) is True

    assert PolyMatrix([[x, y]]) != PolyMatrix([x, y]) == PolyMatrix([[x], [y]])

    assert PolyMatrix([x], ring=QQ[x]) != PolyMatrix([x], ring=ZZ[x])

    assert PolyMatrix([x]) != Matrix([x])
    assert PolyMatrix([x]).to_Matrix() == Matrix([x])

    assert PolyMatrix([1], x) == PolyMatrix([1], x)
    assert PolyMatrix([1], x) != PolyMatrix([1], y)

