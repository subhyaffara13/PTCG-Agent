
def test_simplify():
    n = Symbol('n')
    f = Function('f')

    M = OperationsOnlyMatrix([[            1/x + 1/y,                 (x + x*y) / x  ],
                [ (f(x) + y*f(x))/f(x), 2 * (1/n - cos(n * pi)/n) / pi ]])
    assert M.simplify() == Matrix([[ (x + y)/(x * y),                        1 + y ],
                        [           1 + y, 2*((1 - 1*cos(pi*n))/(pi*n)) ]])
    eq = (1 + x)**2
    M = OperationsOnlyMatrix([[eq]])
    assert M.simplify() == Matrix([[eq]])
    assert M.simplify(ratio=oo) == Matrix([[eq.simplify(ratio=oo)]])

    # https://github.com/sympy/sympy/issues/19353
    m = Matrix([[30, 2], [3, 4]])
    assert (1/(m.trace())).simplify() == Rational(1, 34)


def test_simplify():
    n = Symbol('n')
    f = Function('f')

    M = Matrix([[            1/x + 1/y,                 (x + x*y) / x  ],
                [ (f(x) + y*f(x))/f(x), 2 * (1/n - cos(n * pi)/n) / pi ]])
    M.simplify()
    assert M == Matrix([[ (x + y)/(x * y),                        1 + y ],
                        [           1 + y, 2*((1 - 1*cos(pi*n))/(pi*n)) ]])
    eq = (1 + x)**2
    M = Matrix([[eq]])
    M.simplify()
    assert M == Matrix([[eq]])
    M.simplify(ratio=oo)
    assert M == Matrix([[eq.simplify(ratio=oo)]])


def test_simplify():
    n = Symbol('n')
    f = Function('f')

    M = Matrix([[            1/x + 1/y,                 (x + x*y) / x  ],
                [ (f(x) + y*f(x))/f(x), 2 * (1/n - cos(n * pi)/n) / pi ]])
    M.simplify()
    assert M == Matrix([[ (x + y)/(x * y),                        1 + y ],
                        [           1 + y, 2*((1 - 1*cos(pi*n))/(pi*n)) ]])
    eq = (1 + x)**2
    M = Matrix([[eq]])
    M.simplify()
    assert M == Matrix([[eq]])
    M.simplify(ratio=oo)
    assert M == Matrix([[eq.simplify(ratio=oo)]])

    n = Symbol('n')
    f = Function('f')

    M = ImmutableMatrix([
        [            1/x + 1/y,                 (x + x*y) / x  ],
        [ (f(x) + y*f(x))/f(x), 2 * (1/n - cos(n * pi)/n) / pi ]
    ])
    assert M.simplify() == Matrix([
        [ (x + y)/(x * y),                        1 + y ],
        [           1 + y, 2*((1 - 1*cos(pi*n))/(pi*n)) ]
    ])

    eq = (1 + x)**2
    M = ImmutableMatrix([[eq]])
    assert M.simplify() == Matrix([[eq]])
    assert M.simplify(ratio=oo) == Matrix([[eq.simplify(ratio=oo)]])

    assert simplify(ImmutableMatrix([[sin(x)**2 + cos(x)**2]])) == \
                    ImmutableMatrix([[1]])

    # https://github.com/sympy/sympy/issues/19353
    m = Matrix([[30, 2], [3, 4]])
    assert (1/(m.trace())).simplify() == Rational(1, 34)


def test_simplify():
    x, y = R2_r.coord_functions()
    dx, dy = R2_r.base_oneforms()
    ex, ey = R2_r.base_vectors()
    assert simplify(x) == x
    assert simplify(x*y) == x*y
    assert simplify(dx*dy) == dx*dy
    assert simplify(ex*ey) == ex*ey
    assert ((1-x)*dx)/(1-x)**2 == dx/(1-x)


def test_simplify():
    assert simplify(A*B - B*A) == A*B - B*A

