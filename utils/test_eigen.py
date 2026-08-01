
def test_eigen():
    R = Rational
    M = Matrix.eye(3)
    assert M.eigenvals(multiple=False) == {S.One: 3}
    assert M.eigenvals(multiple=True) == [1, 1, 1]

    assert M.eigenvects() == (
        [(1, 3, [Matrix([1, 0, 0]),
                 Matrix([0, 1, 0]),
                 Matrix([0, 0, 1])])])

    assert M.left_eigenvects() == (
        [(1, 3, [Matrix([[1, 0, 0]]),
                 Matrix([[0, 1, 0]]),
                 Matrix([[0, 0, 1]])])])

    M = Matrix([[0, 1, 1],
                [1, 0, 0],
                [1, 1, 1]])

    assert M.eigenvals() == {2*S.One: 1, -S.One: 1, S.Zero: 1}

    assert M.eigenvects() == (
        [
            (-1, 1, [Matrix([-1, 1, 0])]),
            ( 0, 1, [Matrix([0, -1, 1])]),
            ( 2, 1, [Matrix([R(2, 3), R(1, 3), 1])])
        ])

    assert M.left_eigenvects() == (
        [
            (-1, 1, [Matrix([[-2, 1, 1]])]),
            (0, 1, [Matrix([[-1, -1, 1]])]),
            (2, 1, [Matrix([[1, 1, 1]])])
        ])

    a = Symbol('a')
    M = Matrix([[a, 0],
                [0, 1]])

    assert M.eigenvals() == {a: 1, S.One: 1}

    M = Matrix([[1, -1],
                [1,  3]])
    assert M.eigenvects() == ([(2, 2, [Matrix(2, 1, [-1, 1])])])
    assert M.left_eigenvects() == ([(2, 2, [Matrix([[1, 1]])])])

    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    a = R(15, 2)
    b = 3*33**R(1, 2)
    c = R(13, 2)
    d = (R(33, 8) + 3*b/8)
    e = (R(33, 8) - 3*b/8)

    def NS(e, n):
        return str(N(e, n))
    r = [
        (a - b/2, 1, [Matrix([(12 + 24/(c - b/2))/((c - b/2)*e) + 3/(c - b/2),
                              (6 + 12/(c - b/2))/e, 1])]),
        (      0, 1, [Matrix([1, -2, 1])]),
        (a + b/2, 1, [Matrix([(12 + 24/(c + b/2))/((c + b/2)*d) + 3/(c + b/2),
                              (6 + 12/(c + b/2))/d, 1])]),
    ]
    r1 = [(NS(r[i][0], 2), NS(r[i][1], 2),
        [NS(j, 2) for j in r[i][2][0]]) for i in range(len(r))]
    r = M.eigenvects()
    r2 = [(NS(r[i][0], 2), NS(r[i][1], 2),
        [NS(j, 2) for j in r[i][2][0]]) for i in range(len(r))]
    assert sorted(r1) == sorted(r2)

    eps = Symbol('eps', real=True)

    M = Matrix([[abs(eps), I*eps    ],
                [-I*eps,   abs(eps) ]])

    assert M.eigenvects() == (
        [
            ( 0, 1, [Matrix([[-I*eps/abs(eps)], [1]])]),
            ( 2*abs(eps), 1, [ Matrix([[I*eps/abs(eps)], [1]]) ] ),
        ])

    assert M.left_eigenvects() == (
        [
            (0, 1, [Matrix([[I*eps/Abs(eps), 1]])]),
            (2*Abs(eps), 1, [Matrix([[-I*eps/Abs(eps), 1]])])
        ])

    M = Matrix(3, 3, [1, 2, 0, 0, 3, 0, 2, -4, 2])
    M._eigenvects = M.eigenvects(simplify=False)
    assert max(i.q for i in M._eigenvects[0][2][0]) > 1
    M._eigenvects = M.eigenvects(simplify=True)
    assert max(i.q for i in M._eigenvects[0][2][0]) == 1

    M = Matrix([[Rational(1, 4), 1], [1, 1]])
    assert M.eigenvects() == [
        (Rational(5, 8) - sqrt(73)/8, 1, [Matrix([[-sqrt(73)/8 - Rational(3, 8)], [1]])]),
        (Rational(5, 8) + sqrt(73)/8, 1, [Matrix([[Rational(-3, 8) + sqrt(73)/8], [1]])])]

    # issue 10719
    assert Matrix([]).eigenvals() == {}
    assert Matrix([]).eigenvals(multiple=True) == []
    assert Matrix([]).eigenvects() == []

    # issue 15119
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 2], [0, 4], [0, 0]]).eigenvals())
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 0], [3, 4], [5, 6]]).eigenvals())
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 2, 3], [0, 5, 6]]).eigenvals())
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 0, 0], [4, 5, 0]]).eigenvals())
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 2, 3], [0, 5, 6]]).eigenvals(
               error_when_incomplete = False))
    raises(NonSquareMatrixError,
           lambda: Matrix([[1, 0, 0], [4, 5, 0]]).eigenvals(
               error_when_incomplete = False))

    m = Matrix([[1, 2], [3, 4]])
    assert isinstance(m.eigenvals(simplify=True, multiple=False), dict)
    assert isinstance(m.eigenvals(simplify=True, multiple=True), list)
    assert isinstance(m.eigenvals(simplify=lambda x: x, multiple=False), dict)
    assert isinstance(m.eigenvals(simplify=lambda x: x, multiple=True), list)

