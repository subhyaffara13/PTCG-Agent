
def test_polymatrix_constructor():
    M1 = PolyMatrix([[x, y]], ring=QQ[x,y])
    assert M1.ring == QQ[x,y]
    assert M1.domain == QQ
    assert M1.gens == (x, y)
    assert M1.shape == (1, 2)
    assert M1.rows == 1
    assert M1.cols == 2
    assert len(M1) == 2
    assert list(M1) == [Poly(x, (x, y), domain=QQ), Poly(y, (x, y), domain=QQ)]

    M2 = PolyMatrix([[x, y]], ring=QQ[x][y])
    assert M2.ring == QQ[x][y]
    assert M2.domain == QQ[x]
    assert M2.gens == (y,)
    assert M2.shape == (1, 2)
    assert M2.rows == 1
    assert M2.cols == 2
    assert len(M2) == 2
    assert list(M2) == [Poly(x, (y,), domain=QQ[x]), Poly(y, (y,), domain=QQ[x])]

    assert PolyMatrix([[x, y]], y) == PolyMatrix([[x, y]], ring=ZZ.frac_field(x)[y])
    assert PolyMatrix([[x, y]], ring='ZZ[x,y]') == PolyMatrix([[x, y]], ring=ZZ[x,y])

    assert PolyMatrix([[x, y]], (x, y)) == PolyMatrix([[x, y]], ring=QQ[x,y])
    assert PolyMatrix([[x, y]], x, y) == PolyMatrix([[x, y]], ring=QQ[x,y])
    assert PolyMatrix([x, y]) == PolyMatrix([[x], [y]], ring=QQ[x,y])
    assert PolyMatrix(1, 2, [x, y]) == PolyMatrix([[x, y]], ring=QQ[x,y])
    assert PolyMatrix(1, 2, lambda i,j: [x,y][j]) == PolyMatrix([[x, y]], ring=QQ[x,y])
    assert PolyMatrix(0, 2, [], x, y).shape == (0, 2)
    assert PolyMatrix(2, 0, [], x, y).shape == (2, 0)
    assert PolyMatrix([[], []], x, y).shape == (2, 0)
    assert PolyMatrix(ring=QQ[x,y]) == PolyMatrix(0, 0, [], ring=QQ[x,y]) == PolyMatrix([], ring=QQ[x,y])
    raises(TypeError, lambda: PolyMatrix())
    raises(TypeError, lambda: PolyMatrix(1))

    assert PolyMatrix([Poly(x), Poly(y)]) == PolyMatrix([[x], [y]], ring=ZZ[x,y])

    # XXX: Maybe a bug in parallel_poly_from_expr (x lost from gens and domain):
    assert PolyMatrix([Poly(y, x), 1]) == PolyMatrix([[y], [1]], ring=QQ[y])

