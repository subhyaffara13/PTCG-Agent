
def test_Sum_doit():
    assert Sum(n*Integral(a**2), (n, 0, 2)).doit() == a**3
    assert Sum(n*Integral(a**2), (n, 0, 2)).doit(deep=False) == \
        3*Integral(a**2)
    assert summation(n*Integral(a**2), (n, 0, 2)) == 3*Integral(a**2)

    # test nested sum evaluation
    s = Sum( Sum( Sum(2,(z,1,n+1)), (y,x+1,n)), (x,1,n))
    assert 0 == (s.doit() - n*(n+1)*(n-1)).factor()

    # Integer assumes finite
    assert Sum(KroneckerDelta(x, y), (x, -oo, oo)).doit() == Piecewise((1, And(-oo < y, y < oo)), (0, True))
    assert Sum(KroneckerDelta(m, n), (m, -oo, oo)).doit() == 1
    assert Sum(m*KroneckerDelta(x, y), (x, -oo, oo)).doit() == Piecewise((m, And(-oo < y, y < oo)), (0, True))
    assert Sum(x*KroneckerDelta(m, n), (m, -oo, oo)).doit() == x
    assert Sum(Sum(KroneckerDelta(m, n), (m, 1, 3)), (n, 1, 3)).doit() == 3
    assert Sum(Sum(KroneckerDelta(k, m), (m, 1, 3)), (n, 1, 3)).doit() == \
           3 * Piecewise((1, And(1 <= k, k <= 3)), (0, True))
    assert Sum(f(n) * Sum(KroneckerDelta(m, n), (m, 0, oo)), (n, 1, 3)).doit() == \
           f(1) + f(2) + f(3)
    assert Sum(f(n) * Sum(KroneckerDelta(m, n), (m, 0, oo)), (n, 1, oo)).doit() == \
           Sum(f(n), (n, 1, oo))

    # issue 2597
    nmax = symbols('N', integer=True, positive=True)
    pw = Piecewise((1, And(1 <= n, n <= nmax)), (0, True))
    assert Sum(pw, (n, 1, nmax)).doit() == Sum(Piecewise((1, nmax >= n),
                    (0, True)), (n, 1, nmax))

    q, s = symbols('q, s')
    assert summation(1/n**(2*s), (n, 1, oo)) == Piecewise((zeta(2*s), 2*re(s) > 1),
        (Sum(n**(-2*s), (n, 1, oo)), True))
    assert summation(1/(n+1)**s, (n, 0, oo)) == Piecewise((zeta(s), re(s) > 1),
        (Sum((n + 1)**(-s), (n, 0, oo)), True))
    assert summation(1/(n+q)**s, (n, 0, oo)) == Piecewise(
        (zeta(s, q), And(~Contains(-q, S.Naturals0), re(s) > 1)),
        (Sum((n + q)**(-s), (n, 0, oo)), True))
    assert summation(1/(n+q)**s, (n, q, oo)) == Piecewise(
        (zeta(s, 2*q), And(~Contains(-2*q, S.Naturals0), re(s) > 1)),
        (Sum((n + q)**(-s), (n, q, oo)), True))
    assert summation(1/n**2, (n, 1, oo)) == zeta(2)
    assert summation(1/n**s, (n, 0, oo)) == Sum(n**(-s), (n, 0, oo))
    assert summation(1/(n+1)**(2+I), (n, 0, oo)) == zeta(2+I)
    t = symbols('t', real=True, positive=True)
    assert summation(1/(n+I)**(t+1), (n, 0, oo)) == zeta(t+1, I)

