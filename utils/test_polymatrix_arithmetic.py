
def test_polymatrix_arithmetic():
    M = PolyMatrix([[1, 2], [3, 4]], x)
    assert M + M == PolyMatrix([[2, 4], [6, 8]], x)
    assert M - M == PolyMatrix([[0, 0], [0, 0]], x)
    assert -M == PolyMatrix([[-1, -2], [-3, -4]], x)
    raises(TypeError, lambda: M + 1)
    raises(TypeError, lambda: M - 1)
    raises(TypeError, lambda: 1 + M)
    raises(TypeError, lambda: 1 - M)

    assert M * M == PolyMatrix([[7, 10], [15, 22]], x)
    assert 2 * M == PolyMatrix([[2, 4], [6, 8]], x)
    assert M * 2 == PolyMatrix([[2, 4], [6, 8]], x)
    assert S(2) * M == PolyMatrix([[2, 4], [6, 8]], x)
    assert M * S(2) == PolyMatrix([[2, 4], [6, 8]], x)
    raises(TypeError, lambda: [] * M)
    raises(TypeError, lambda: M * [])
    M2 = PolyMatrix([[1, 2]], ring=ZZ[x])
    assert S.Half * M2 == PolyMatrix([[S.Half, 1]], ring=QQ[x])
    assert M2 * S.Half == PolyMatrix([[S.Half, 1]], ring=QQ[x])

    assert M / 2 == PolyMatrix([[S(1)/2, 1], [S(3)/2, 2]], x)
    assert M / Poly(2, x) == PolyMatrix([[S(1)/2, 1], [S(3)/2, 2]], x)
    raises(TypeError, lambda: M / [])

