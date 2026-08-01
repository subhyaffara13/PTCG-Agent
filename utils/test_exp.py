
def test_exp():
    e = exp(x).lseries(x)
    assert next(e) == 1
    assert next(e) == x
    assert next(e) == x**2/2
    assert next(e) == x**3/6


def test_exp():
    e = (1 + x)**(1/x)
    assert e.nseries(x, n=3) == exp(1) - x*exp(1)/2 + 11*exp(1)*x**2/24 + O(x**3)


def test_exp():
    e1 = exp(x).series(x, 0)
    e2 = series(exp(x), x, 0)
    assert e1 == e2


def test_exp():
    R, x = ring('x', QQ)
    p = x + x**4
    for h in [10, 30]:
        q = rs_series_inversion(1 + p, x, h) - 1
        p1 = rs_exp(q, x, h)
        q1 = rs_log(p1, x, h)
        assert q1 == q
    p1 = rs_exp(p, x, 30)
    assert p1.coeff(x**29) == QQ(74274246775059676726972369, 353670479749588078181744640000)
    prec = 21
    p = rs_log(1 + x, x, prec)
    p1 = rs_exp(p, x, prec)
    assert p1 == x + 1

    # Constant term in series
    a = symbols('a')
    R, x, y = ring('x, y', QQ[exp(a), a])
    assert rs_exp(x + a, x, 5) == exp(a)*x**4/24 + exp(a)*x**3/6 + \
        exp(a)*x**2/2 + exp(a)*x + exp(a)
    assert rs_exp(x + x**2*y + a, x, 5) == exp(a)*x**4*y**2/2 + \
            exp(a)*x**4*y/2 + exp(a)*x**4/24 + exp(a)*x**3*y + \
            exp(a)*x**3/6 + exp(a)*x**2*y + exp(a)*x**2/2 + exp(a)*x + exp(a)

    R, x, y = ring('x, y', EX)
    assert rs_exp(x + a, x, 5) ==  EX(exp(a)/24)*x**4 + EX(exp(a)/6)*x**3 + \
        EX(exp(a)/2)*x**2 + EX(exp(a))*x + EX(exp(a))
    assert rs_exp(x + x**2*y + a, x, 5) == EX(exp(a)/2)*x**4*y**2 + \
        EX(exp(a)/2)*x**4*y + EX(exp(a)/24)*x**4 + EX(exp(a))*x**3*y + \
        EX(exp(a)/6)*x**3 + EX(exp(a))*x**2*y + EX(exp(a)/2)*x**2 + \
        EX(exp(a))*x + EX(exp(a))


def test_exp():
    a = exp(interval(-np.inf, 0))
    assert a.start == np.exp(-np.inf)
    assert a.end == np.exp(0)
    a = exp(interval(1, 2))
    assert a.start == np.exp(1)
    assert a.end == np.exp(2)
    a = exp(1)
    assert a.start == np.exp(1)
    assert a.end == np.exp(1)


def test_exp():
    m = Matrix([[3, 4], [0, -2]])
    m_exp = Matrix([[exp(3), -4*exp(-2)/5 + 4*exp(3)/5], [0, exp(-2)]])
    assert m.exp() == m_exp
    assert exp(m) == m_exp

    m = Matrix([[1, 0], [0, 1]])
    assert m.exp() == Matrix([[E, 0], [0, E]])
    assert exp(m) == Matrix([[E, 0], [0, E]])

    m = Matrix([[1, -1], [1, 1]])
    assert m.exp() == Matrix([[E*cos(1), -E*sin(1)], [E*sin(1), E*cos(1)]])


def test_exp():
    m = Matrix([[3, 4], [0, -2]])
    m_exp = Matrix([[exp(3), -4*exp(-2)/5 + 4*exp(3)/5], [0, exp(-2)]])
    assert m.exp() == m_exp
    assert exp(m) == m_exp

    m = Matrix([[1, 0], [0, 1]])
    assert m.exp() == Matrix([[E, 0], [0, E]])
    assert exp(m) == Matrix([[E, 0], [0, E]])

    m = Matrix([[1, -1], [1, 1]])
    assert m.exp() == Matrix([[E*cos(1), -E*sin(1)], [E*sin(1), E*cos(1)]])


def test_exp():
    A = MatrixSymbol('A', 2, 2)
    B = MatrixSymbol('B', 2, 2)
    expr1 = exp(A)*exp(B)
    expr2 = exp(B)*exp(A)
    assert expr1 != expr2
    assert expr1 - expr2 != 0
    assert not isinstance(expr1, exp)
    assert not isinstance(expr2, exp)


def test_exp():
    x = Symbol('x', integer=True)
    assert refine(exp(pi*I*2*x)) == 1
    assert refine(exp(pi*I*2*(x + S.Half))) == -1
    assert refine(exp(pi*I*2*(x + Rational(1, 4)))) == I
    assert refine(exp(pi*I*2*(x + Rational(3, 4)))) == -I


def test_exp():
    assert exp(0) == 1
    assert exp(10000).ae(mpf('8.8068182256629215873e4342'))
    assert exp(-10000).ae(mpf('1.1354838653147360985e-4343'))
    a = exp(mpf((1, 8198646019315405, -53, 53)))
    assert(a.bc == bitcount(a.man))
    mp.prec = 67
    a = exp(mpf((1, 1781864658064754565, -60, 61)))
    assert(a.bc == bitcount(a.man))
    mp.prec = 53
    assert exp(ln2 * 10).ae(1024)
    assert exp(2+2j).ae(cmath.exp(2+2j))

