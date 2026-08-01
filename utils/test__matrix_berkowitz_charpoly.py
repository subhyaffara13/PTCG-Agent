
def test_Matrix_berkowitz_charpoly():
    UA, K_i, K_w = symbols('UA K_i K_w')

    A = Matrix([[-K_i - UA + K_i**2/(K_i + K_w),       K_i*K_w/(K_i + K_w)],
                [           K_i*K_w/(K_i + K_w), -K_w + K_w**2/(K_i + K_w)]])

    charpoly = A.charpoly(x)

    assert charpoly == \
        Poly(x**2 + (K_i*UA + K_w*UA + 2*K_i*K_w)/(K_i + K_w)*x +
        K_i*K_w*UA/(K_i + K_w), x, domain='ZZ(K_i,K_w,UA)')

    assert type(charpoly) is PurePoly

    A = Matrix([[1, 3], [2, 0]])
    assert A.charpoly() == A.charpoly(x) == PurePoly(x**2 - x - 6)

    A = Matrix([[1, 2], [x, 0]])
    p = A.charpoly(x)
    assert p.gen != x
    assert p.as_expr().subs(p.gen, x) == x**2 - 3*x


def test_Matrix_berkowitz_charpoly():
    UA, K_i, K_w = symbols('UA K_i K_w')

    A = Matrix([[-K_i - UA + K_i**2/(K_i + K_w),       K_i*K_w/(K_i + K_w)],
                [           K_i*K_w/(K_i + K_w), -K_w + K_w**2/(K_i + K_w)]])

    charpoly = A.charpoly(x)

    assert charpoly == \
        Poly(x**2 + (K_i*UA + K_w*UA + 2*K_i*K_w)/(K_i + K_w)*x +
        K_i*K_w*UA/(K_i + K_w), x, domain='ZZ(K_i,K_w,UA)')

    assert type(charpoly) is PurePoly

    A = Matrix([[1, 3], [2, 0]])
    assert A.charpoly() == A.charpoly(x) == PurePoly(x**2 - x - 6)

    A = Matrix([[1, 2], [x, 0]])
    p = A.charpoly(x)
    assert p.gen != x
    assert p.as_expr().subs(p.gen, x) == x**2 - 3*x

