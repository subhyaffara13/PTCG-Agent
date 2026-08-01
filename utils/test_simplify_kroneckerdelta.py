
def test_simplify_kroneckerdelta():
    i, j = symbols("i j")
    K = KroneckerDelta

    assert simplify(K(i, j)) == K(i, j)
    assert simplify(K(0, j)) == K(0, j)
    assert simplify(K(i, 0)) == K(i, 0)

    assert simplify(K(0, j).rewrite(Piecewise) * K(1, j)) == 0
    assert simplify(K(1, i) + Piecewise((1, Eq(j, 2)), (0, True))) == K(1, i) + K(2, j)

    # issue 17214
    assert simplify(K(0, j) * K(1, j)) == 0

    n = Symbol('n', integer=True)
    assert simplify(K(0, n) * K(1, n)) == 0

    M = Matrix(4, 4, lambda i, j: K(j - i, n) if i <= j else 0)
    assert simplify(M**2) == Matrix([[K(0, n), 0, K(1, n), 0],
                                     [0, K(0, n), 0, K(1, n)],
                                     [0, 0, K(0, n), 0],
                                     [0, 0, 0, K(0, n)]])
    assert simplify(eye(1) * KroneckerDelta(0, n) *
                    KroneckerDelta(1, n)) == Matrix([[0]])

    assert simplify(S.Infinity * KroneckerDelta(0, n) *
                    KroneckerDelta(1, n)) is S.NaN

