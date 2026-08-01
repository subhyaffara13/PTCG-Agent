
def test_solve_Matrix():
    # https://github.com/sympy/sympy/issues/3870
    a, b, c, d = symbols('a b c d')
    A = Matrix(2, 2, [a, b, c, d])
    B = Matrix(2, 2, [0, 2, -3, 0])
    C = Matrix(2, 2, [1, 2, 3, 4])

    assert solve(A*B - C, [a, b, c, d]) == {a: 1, b: Rational(-1, 3), c: 2, d: -1}
    assert solve([A*B - C], [a, b, c, d]) == {a: 1, b: Rational(-1, 3), c: 2, d: -1}
    assert solve(Eq(A*B, C), [a, b, c, d]) == {a: 1, b: Rational(-1, 3), c: 2, d: -1}

    assert solve([A*B - B*A], [a, b, c, d]) == {a: d, b: Rational(-2, 3)*c}
    assert solve([A*C - C*A], [a, b, c, d]) == {a: d - c, b: Rational(2, 3)*c}
    assert solve([A*B - B*A, A*C - C*A], [a, b, c, d]) == {a: d, b: 0, c: 0}

    assert solve([Eq(A*B, B*A)], [a, b, c, d]) == {a: d, b: Rational(-2, 3)*c}
    assert solve([Eq(A*C, C*A)], [a, b, c, d]) == {a: d - c, b: Rational(2, 3)*c}
    assert solve([Eq(A*B, B*A), Eq(A*C, C*A)], [a, b, c, d]) == {a: d, b: 0, c: 0}

    # https://github.com/sympy/sympy/issues/27854
    m, n = symbols("m n")
    A = MatrixSymbol("A", m, n)
    x = MatrixSymbol("x", n, 1)
    b = MatrixSymbol('b', m, 1)
    r = A * x - b
    f = r.T * r
    grad_f = f.diff(x)
    raises(ValueError, lambda: solve(grad_f, x))

