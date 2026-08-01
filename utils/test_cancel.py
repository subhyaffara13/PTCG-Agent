
def test_cancel():
    assert cancel(0) == 0
    assert cancel(7) == 7
    assert cancel(x) == x

    assert cancel(oo) is oo

    raises(ValueError, lambda: cancel((1, 2, 3)))

    # test first tuple returnr
    assert (t:=cancel((2, 3))) == (1, 2, 3)
    assert isinstance(t, tuple)

    # tests 2nd tuple return
    assert (t:=cancel((1, 0), x)) == (1, 1, 0)
    assert isinstance(t, tuple)
    assert cancel((0, 1), x) == (1, 0, 1)

    f, g, p, q = 4*x**2 - 4, 2*x - 2, 2*x + 2, 1
    F, G, P, Q = [ Poly(u, x) for u in (f, g, p, q) ]

    assert F.cancel(G) == (1, P, Q)
    assert cancel((f, g)) == (1, p, q)
    assert cancel((f, g), x) == (1, p, q)
    assert cancel((f, g), (x,)) == (1, p, q)
    # tests 3rd tuple return
    assert (t:=cancel((F, G))) == (1, P, Q)
    assert isinstance(t, tuple)
    assert cancel((f, g), polys=True) == (1, P, Q)
    assert cancel((F, G), polys=False) == (1, p, q)

    f = (x**2 - 2)/(x + sqrt(2))

    assert cancel(f) == f
    assert cancel(f, greedy=False) == x - sqrt(2)

    f = (x**2 - 2)/(x - sqrt(2))

    assert cancel(f) == f
    assert cancel(f, greedy=False) == x + sqrt(2)

    assert cancel((x**2/4 - 1, x/2 - 1)) == (1, x + 2, 2)
    # assert cancel((x**2/4 - 1, x/2 - 1)) == (S.Half, x + 2, 1)

    assert cancel((x**2 - y)/(x - y)) == 1/(x - y)*(x**2 - y)

    assert cancel((x**2 - y**2)/(x - y), x) == x + y
    assert cancel((x**2 - y**2)/(x - y), y) == x + y
    assert cancel((x**2 - y**2)/(x - y)) == x + y

    assert cancel((x**3 - 1)/(x**2 - 1)) == (x**2 + x + 1)/(x + 1)
    assert cancel((x**3/2 - S.Half)/(x**2 - 1)) == (x**2 + x + 1)/(2*x + 2)

    assert cancel((exp(2*x) + 2*exp(x) + 1)/(exp(x) + 1)) == exp(x) + 1

    f = Poly(x**2 - a**2, x)
    g = Poly(x - a, x)

    F = Poly(x + a, x, domain='ZZ[a]')
    G = Poly(1, x, domain='ZZ[a]')

    assert cancel((f, g)) == (1, F, G)

    f = x**3 + (sqrt(2) - 2)*x**2 - (2*sqrt(2) + 3)*x - 3*sqrt(2)
    g = x**2 - 2

    assert cancel((f, g), extension=True) == (1, x**2 - 2*x - 3, x - sqrt(2))

    f = Poly(-2*x + 3, x)
    g = Poly(-x**9 + x**8 + x**6 - x**5 + 2*x**2 - 3*x + 1, x)

    assert cancel((f, g)) == (1, -f, -g)

    f = Poly(x/3 + 1, x)
    g = Poly(x/7 + 1, x)

    assert f.cancel(g) == (S(7)/3,
        Poly(x + 3, x, domain=QQ),
        Poly(x + 7, x, domain=QQ))
    assert f.cancel(g, include=True) == (
        Poly(7*x + 21, x, domain=QQ),
        Poly(3*x + 21, x, domain=QQ))

    pairs = [
        (1 + x, 1 + x, 1, 1, 1),
        (1 + x, 1 - x, -1, -1-x, -1+x),
        (1 - x, 1 + x, -1, 1-x, 1+x),
        (1 - x, 1 - x, 1, 1, 1),
    ]
    for f, g, coeff, p, q in pairs:
        assert cancel((f, g)) == (1, p, q)
        pf = Poly(f, x)
        pg = Poly(g, x)
        pp = Poly(p, x)
        pq = Poly(q, x)
        assert pf.cancel(pg) == (coeff, coeff*pp, pq)
        assert pf.rep.cancel(pg.rep) == (pp.rep, pq.rep)
        assert pf.rep.cancel(pg.rep, include=True) == (pp.rep, pq.rep)

    f = Poly(y, y, domain='ZZ(x)')
    g = Poly(1, y, domain='ZZ[x]')

    assert f.cancel(
        g) == (1, Poly(y, y, domain='ZZ(x)'), Poly(1, y, domain='ZZ(x)'))
    assert f.cancel(g, include=True) == (
        Poly(y, y, domain='ZZ(x)'), Poly(1, y, domain='ZZ(x)'))

    f = Poly(5*x*y + x, y, domain='ZZ(x)')
    g = Poly(2*x**2*y, y, domain='ZZ(x)')

    assert f.cancel(g, include=True) == (
        Poly(5*y + 1, y, domain='ZZ(x)'), Poly(2*x*y, y, domain='ZZ(x)'))

    f = -(-2*x - 4*y + 0.005*(z - y)**2)/((z - y)*(-z + y + 2))
    assert cancel(f).is_Mul == True

    P = tanh(x - 3.0)
    Q = tanh(x + 3.0)
    f = ((-2*P**2 + 2)*(-P**2 + 1)*Q**2/2 + (-2*P**2 + 2)*(-2*Q**2 + 2)*P*Q - (-2*P**2 + 2)*P**2*Q**2 + (-2*Q**2 + 2)*(-Q**2 + 1)*P**2/2 - (-2*Q**2 + 2)*P**2*Q**2)/(2*sqrt(P**2*Q**2 + 0.0001)) \
      + (-(-2*P**2 + 2)*P*Q**2/2 - (-2*Q**2 + 2)*P**2*Q/2)*((-2*P**2 + 2)*P*Q**2/2 + (-2*Q**2 + 2)*P**2*Q/2)/(2*(P**2*Q**2 + 0.0001)**Rational(3, 2))
    assert cancel(f).is_Mul == True

    # issue 7022
    A = Symbol('A', commutative=False)
    p1 = Piecewise((A*(x**2 - 1)/(x + 1), x > 1), ((x + 2)/(x**2 + 2*x), True))
    p2 = Piecewise((A*(x - 1), x > 1), (1/x, True))
    assert cancel(p1) == p2
    assert cancel(2*p1) == 2*p2
    assert cancel(1 + p1) == 1 + p2
    assert cancel((x**2 - 1)/(x + 1)*p1) == (x - 1)*p2
    assert cancel((x**2 - 1)/(x + 1) + p1) == (x - 1) + p2
    p3 = Piecewise(((x**2 - 1)/(x + 1), x > 1), ((x + 2)/(x**2 + 2*x), True))
    p4 = Piecewise(((x - 1), x > 1), (1/x, True))
    assert cancel(p3) == p4
    assert cancel(2*p3) == 2*p4
    assert cancel(1 + p3) == 1 + p4
    assert cancel((x**2 - 1)/(x + 1)*p3) == (x - 1)*p4
    assert cancel((x**2 - 1)/(x + 1) + p3) == (x - 1) + p4

    # issue 4077
    q = S('''(2*1*(x - 1/x)/(x*(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x -
        1/x)) - 2/x)) - 2*1*((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x -
        1/x)))*((-x + 1/x)*((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x -
        1/x)))/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) -
        2/x) + 1)*((x - 1/x)/((x - 1/x)**2) - ((x - 1/x)/((x*(x - 1/x)**2)) -
        1/(x*(x - 1/x)))**2/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x
        - 1/x)) - 2/x) - 1/(x - 1/x))*(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) -
        1/(x**2*(x - 1/x)) - 2/x)/x - 1/x)*(((-x + 1/x)/((x*(x - 1/x)**2)) +
        1/(x*(x - 1/x)))*((-(x - 1/x)/(x*(x - 1/x)) - 1/x)*((x - 1/x)/((x*(x -
        1/x)**2)) - 1/(x*(x - 1/x)))/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) -
        1/(x**2*(x - 1/x)) - 2/x) - 1 + (x - 1/x)/(x - 1/x))/((x*((x -
        1/x)/((x - 1/x)**2) - ((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x -
        1/x)))**2/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) -
        2/x) - 1/(x - 1/x))*(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x
        - 1/x)) - 2/x))) + ((x - 1/x)/((x*(x - 1/x))) + 1/x)/((x*(2*x - (-x +
        1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) - 2/x))) + 1/x)/(2*x +
        2*((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x - 1/x)))*((-(x - 1/x)/(x*(x
        - 1/x)) - 1/x)*((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x - 1/x)))/(2*x -
        (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) - 2/x) - 1 + (x -
        1/x)/(x - 1/x))/((x*((x - 1/x)/((x - 1/x)**2) - ((x - 1/x)/((x*(x -
        1/x)**2)) - 1/(x*(x - 1/x)))**2/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2)
        - 1/(x**2*(x - 1/x)) - 2/x) - 1/(x - 1/x))*(2*x - (-x + 1/x)/(x**2*(x
        - 1/x)**2) - 1/(x**2*(x - 1/x)) - 2/x))) - 2*((x - 1/x)/((x*(x -
        1/x))) + 1/x)/(x*(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x -
        1/x)) - 2/x)) - 2/x) - ((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x -
        1/x)))*((-x + 1/x)*((x - 1/x)/((x*(x - 1/x)**2)) - 1/(x*(x -
        1/x)))/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) -
        2/x) + 1)/(x*((x - 1/x)/((x - 1/x)**2) - ((x - 1/x)/((x*(x - 1/x)**2))
        - 1/(x*(x - 1/x)))**2/(2*x - (-x + 1/x)/(x**2*(x - 1/x)**2) -
        1/(x**2*(x - 1/x)) - 2/x) - 1/(x - 1/x))*(2*x - (-x + 1/x)/(x**2*(x -
        1/x)**2) - 1/(x**2*(x - 1/x)) - 2/x)) + (x - 1/x)/((x*(2*x - (-x +
        1/x)/(x**2*(x - 1/x)**2) - 1/(x**2*(x - 1/x)) - 2/x))) - 1/x''',
        evaluate=False)
    assert cancel(q, _signsimp=False) is S.NaN
    assert q.subs(x, 2) is S.NaN
    assert signsimp(q) is S.NaN

    # issue 9363
    M = MatrixSymbol('M', 5, 5)
    assert cancel(M[0,0] + 7) == M[0,0] + 7
    expr = sin(M[1, 4] + M[2, 1] * 5 * M[4, 0]) - 5 * M[1, 2] / z
    assert cancel(expr) == (z*sin(M[1, 4] + M[2, 1] * 5 * M[4, 0]) - 5 * M[1, 2]) / z

    assert cancel((x**2 + 1)/(x - I)) == x + I


def test_cancel():
    assert cancel(A*B - B*A) == A*B - B*A
    assert cancel(A*B*(x - 1)) == A*B*(x - 1)
    assert cancel(A*B*(x**2 - 1)/(x + 1)) == A*B*(x - 1)
    assert cancel(A*B*(x**2 - 1)/(x + 1) - B*A*(x - 1)) == A*B*(x - 1) + (1 - x)*B*A

