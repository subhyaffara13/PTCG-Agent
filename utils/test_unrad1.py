
def test_unrad1():
    raises(NotImplementedError, lambda:
        unrad(sqrt(x) + sqrt(x + 1) + sqrt(1 - sqrt(x)) + 3))
    raises(NotImplementedError, lambda:
        unrad(sqrt(x) + (x + 1)**Rational(1, 3) + 2*sqrt(y)))

    s = symbols('s', cls=Dummy)

    # checkers to deal with possibility of answer coming
    # back with a sign change (cf issue 5203)
    def check(rv, ans):
        assert bool(rv[1]) == bool(ans[1])
        if ans[1]:
            return s_check(rv, ans)
        e = rv[0].expand()
        a = ans[0].expand()
        return e in [a, -a] and rv[1] == ans[1]

    def s_check(rv, ans):
        # get the dummy
        rv = list(rv)
        d = rv[0].atoms(Dummy)
        reps = list(zip(d, [s]*len(d)))
        # replace s with this dummy
        rv = (rv[0].subs(reps).expand(), [rv[1][0].subs(reps), rv[1][1].subs(reps)])
        ans = (ans[0].subs(reps).expand(), [ans[1][0].subs(reps), ans[1][1].subs(reps)])
        return str(rv[0]) in [str(ans[0]), str(-ans[0])] and \
            str(rv[1]) == str(ans[1])

    assert unrad(1) is None
    assert check(unrad(sqrt(x)),
        (x, []))
    assert check(unrad(sqrt(x) + 1),
        (x - 1, []))
    assert check(unrad(sqrt(x) + root(x, 3) + 2),
        (s**3 + s**2 + 2, [s, s**6 - x]))
    assert check(unrad(sqrt(x)*root(x, 3) + 2),
        (x**5 - 64, []))
    assert check(unrad(sqrt(x) + (x + 1)**Rational(1, 3)),
        (x**3 - (x + 1)**2, []))
    assert check(unrad(sqrt(x) + sqrt(x + 1) + sqrt(2*x)),
        (-2*sqrt(2)*x - 2*x + 1, []))
    assert check(unrad(sqrt(x) + sqrt(x + 1) + 2),
        (16*x - 9, []))
    assert check(unrad(sqrt(x) + sqrt(x + 1) + sqrt(1 - x)),
        (5*x**2 - 4*x, []))
    assert check(unrad(a*sqrt(x) + b*sqrt(x) + c*sqrt(y) + d*sqrt(y)),
        ((a*sqrt(x) + b*sqrt(x))**2 - (c*sqrt(y) + d*sqrt(y))**2, []))
    assert check(unrad(sqrt(x) + sqrt(1 - x)),
        (2*x - 1, []))
    assert check(unrad(sqrt(x) + sqrt(1 - x) - 3),
        (x**2 - x + 16, []))
    assert check(unrad(sqrt(x) + sqrt(1 - x) + sqrt(2 + x)),
        (5*x**2 - 2*x + 1, []))
    assert unrad(sqrt(x) + sqrt(1 - x) + sqrt(2 + x) - 3) in [
        (25*x**4 + 376*x**3 + 1256*x**2 - 2272*x + 784, []),
        (25*x**8 - 476*x**6 + 2534*x**4 - 1468*x**2 + 169, [])]
    assert unrad(sqrt(x) + sqrt(1 - x) + sqrt(2 + x) - sqrt(1 - 2*x)) == \
        (41*x**4 + 40*x**3 + 232*x**2 - 160*x + 16, [])  # orig root at 0.487
    assert check(unrad(sqrt(x) + sqrt(x + 1)), (S.One, []))

    eq = sqrt(x) + sqrt(x + 1) + sqrt(1 - sqrt(x))
    assert check(unrad(eq),
        (16*x**2 - 9*x, []))
    assert set(solve(eq, check=False)) == {S.Zero, Rational(9, 16)}
    assert solve(eq) == []
    # but this one really does have those solutions
    assert set(solve(sqrt(x) - sqrt(x + 1) + sqrt(1 - sqrt(x)))) == \
        {S.Zero, Rational(9, 16)}

    assert check(unrad(sqrt(x) + root(x + 1, 3) + 2*sqrt(y), y),
        (S('2*sqrt(x)*(x + 1)**(1/3) + x - 4*y + (x + 1)**(2/3)'), []))
    assert check(unrad(sqrt(x/(1 - x)) + (x + 1)**Rational(1, 3)),
        (x**5 - x**4 - x**3 + 2*x**2 + x - 1, []))
    assert check(unrad(sqrt(x/(1 - x)) + 2*sqrt(y), y),
        (4*x*y + x - 4*y, []))
    assert check(unrad(sqrt(x)*sqrt(1 - x) + 2, x),
        (x**2 - x + 4, []))

    # http://tutorial.math.lamar.edu/
    #        Classes/Alg/SolveRadicalEqns.aspx#Solve_Rad_Ex2_a
    assert solve(Eq(x, sqrt(x + 6))) == [3]
    assert solve(Eq(x + sqrt(x - 4), 4)) == [4]
    assert solve(Eq(1, x + sqrt(2*x - 3))) == []
    assert set(solve(Eq(sqrt(5*x + 6) - 2, x))) == {-S.One, S(2)}
    assert set(solve(Eq(sqrt(2*x - 1) - sqrt(x - 4), 2))) == {S(5), S(13)}
    assert solve(Eq(sqrt(x + 7) + 2, sqrt(3 - x))) == [-6]
    # http://www.purplemath.com/modules/solverad.htm
    assert solve((2*x - 5)**Rational(1, 3) - 3) == [16]
    assert set(solve(x + 1 - root(x**4 + 4*x**3 - x, 4))) == \
        {Rational(-1, 2), Rational(-1, 3)}
    assert set(solve(sqrt(2*x**2 - 7) - (3 - x))) == {-S(8), S(2)}
    assert solve(sqrt(2*x + 9) - sqrt(x + 1) - sqrt(x + 4)) == [0]
    assert solve(sqrt(x + 4) + sqrt(2*x - 1) - 3*sqrt(x - 1)) == [5]
    assert solve(sqrt(x)*sqrt(x - 7) - 12) == [16]
    assert solve(sqrt(x - 3) + sqrt(x) - 3) == [4]
    assert solve(sqrt(9*x**2 + 4) - (3*x + 2)) == [0]
    assert solve(sqrt(x) - 2 - 5) == [49]
    assert solve(sqrt(x - 3) - sqrt(x) - 3) == []
    assert solve(sqrt(x - 1) - x + 7) == [10]
    assert solve(sqrt(x - 2) - 5) == [27]
    assert solve(sqrt(17*x - sqrt(x**2 - 5)) - 7) == [3]
    assert solve(sqrt(x) - sqrt(x - 1) + sqrt(sqrt(x))) == []

    # don't posify the expression in unrad and do use _mexpand
    z = sqrt(2*x + 1)/sqrt(x) - sqrt(2 + 1/x)
    p = posify(z)[0]
    assert solve(p) == []
    assert solve(z) == []
    assert solve(z + 6*I) == [Rational(-1, 11)]
    assert solve(p + 6*I) == []
    # issue 8622
    assert unrad(root(x + 1, 5) - root(x, 3)) == (
        -(x**5 - x**3 - 3*x**2 - 3*x - 1), [])
    # issue #8679
    assert check(unrad(x + root(x, 3) + root(x, 3)**2 + sqrt(y), x),
        (s**3 + s**2 + s + sqrt(y), [s, s**3 - x]))

    # for coverage
    assert check(unrad(sqrt(x) + root(x, 3) + y),
        (s**3 + s**2 + y, [s, s**6 - x]))
    assert solve(sqrt(x) + root(x, 3) - 2) == [1]
    raises(NotImplementedError, lambda:
        solve(sqrt(x) + root(x, 3) + root(x + 1, 5) - 2))
    # fails through a different code path
    raises(NotImplementedError, lambda: solve(-sqrt(2) + cosh(x)/x))
    # unrad some
    assert solve(sqrt(x + root(x, 3))+root(x - y, 5), y) == [
        x + (x**Rational(1, 3) + x)**Rational(5, 2)]
    assert check(unrad(sqrt(x) - root(x + 1, 3)*sqrt(x + 2) + 2),
        (s**10 + 8*s**8 + 24*s**6 - 12*s**5 - 22*s**4 - 160*s**3 - 212*s**2 -
        192*s - 56, [s, s**2 - x]))
    e = root(x + 1, 3) + root(x, 3)
    assert unrad(e) == (2*x + 1, [])
    eq = (sqrt(x) + sqrt(x + 1) + sqrt(1 - x) - 6*sqrt(5)/5)
    assert check(unrad(eq),
        (15625*x**4 + 173000*x**3 + 355600*x**2 - 817920*x + 331776, []))
    assert check(unrad(root(x, 4) + root(x, 4)**3 - 1),
        (s**3 + s - 1, [s, s**4 - x]))
    assert check(unrad(root(x, 2) + root(x, 2)**3 - 1),
        (x**3 + 2*x**2 + x - 1, []))
    assert unrad(x**0.5) is None
    assert check(unrad(t + root(x + y, 5) + root(x + y, 5)**3),
        (s**3 + s + t, [s, s**5 - x - y]))
    assert check(unrad(x + root(x + y, 5) + root(x + y, 5)**3, y),
        (s**3 + s + x, [s, s**5 - x - y]))
    assert check(unrad(x + root(x + y, 5) + root(x + y, 5)**3, x),
        (s**5 + s**3 + s - y, [s, s**5 - x - y]))
    assert check(unrad(root(x - 1, 3) + root(x + 1, 5) + root(2, 5)),
        (s**5 + 5*2**Rational(1, 5)*s**4 + s**3 + 10*2**Rational(2, 5)*s**3 +
        10*2**Rational(3, 5)*s**2 + 5*2**Rational(4, 5)*s + 4, [s, s**3 - x + 1]))
    raises(NotImplementedError, lambda:
        unrad((root(x, 2) + root(x, 3) + root(x, 4)).subs(x, x**5 - x + 1)))

    # the simplify flag should be reset to False for unrad results;
    # if it's not then this next test will take a long time
    assert solve(root(x, 3) + root(x, 5) - 2) == [1]
    eq = (sqrt(x) + sqrt(x + 1) + sqrt(1 - x) - 6*sqrt(5)/5)
    assert check(unrad(eq),
        ((5*x - 4)*(3125*x**3 + 37100*x**2 + 100800*x - 82944), []))
    ans = S('''
        [4/5, -1484/375 + 172564/(140625*(114*sqrt(12657)/78125 +
        12459439/52734375)**(1/3)) +
        4*(114*sqrt(12657)/78125 + 12459439/52734375)**(1/3)]''')
    assert solve(eq) == ans
    # duplicate radical handling
    assert check(unrad(sqrt(x + root(x + 1, 3)) - root(x + 1, 3) - 2),
        (s**3 - s**2 - 3*s - 5, [s, s**3 - x - 1]))
    # cov post-processing
    e = root(x**2 + 1, 3) - root(x**2 - 1, 5) - 2
    assert check(unrad(e),
        (s**5 - 10*s**4 + 39*s**3 - 80*s**2 + 80*s - 30,
        [s, s**3 - x**2 - 1]))

    e = sqrt(x + root(x + 1, 2)) - root(x + 1, 3) - 2
    assert check(unrad(e),
        (s**6 - 2*s**5 - 7*s**4 - 3*s**3 + 26*s**2 + 40*s + 25,
        [s, s**3 - x - 1]))
    assert check(unrad(e, _reverse=True),
        (s**6 - 14*s**5 + 73*s**4 - 187*s**3 + 276*s**2 - 228*s + 89,
        [s, s**2 - x - sqrt(x + 1)]))
    # this one needs r0, r1 reversal to work
    assert check(unrad(sqrt(x + sqrt(root(x, 3) - 1)) - root(x, 6) - 2),
        (s**12 - 2*s**8 - 8*s**7 - 8*s**6 + s**4 + 8*s**3 + 23*s**2 +
        32*s + 17, [s, s**6 - x]))

    # why does this pass
    assert unrad(root(cosh(x), 3)/x*root(x + 1, 5) - 1) == (
        -(x**15 - x**3*cosh(x)**5 - 3*x**2*cosh(x)**5 - 3*x*cosh(x)**5
        - cosh(x)**5), [])
    # and this fail?
    #assert unrad(sqrt(cosh(x)/x) + root(x + 1, 3)*sqrt(x) - 1) == (
    #    -s**6 + 6*s**5 - 15*s**4 + 20*s**3 - 15*s**2 + 6*s + x**5 +
    #    2*x**4 + x**3 - 1, [s, s**2 - cosh(x)/x])

    # watch for symbols in exponents
    assert unrad(S('(x+y)**(2*y/3) + (x+y)**(1/3) + 1')) is None
    assert check(unrad(S('(x+y)**(2*y/3) + (x+y)**(1/3) + 1'), x),
        (s**(2*y) + s + 1, [s, s**3 - x - y]))
    # should _Q be so lenient?
    assert unrad(x**(S.Half/y) + y, x) == (x**(1/y) - y**2, [])

    # This tests two things: that if full unrad is attempted and fails
    # the solution should still be found; also it tests that the use of
    # composite
    assert len(solve(sqrt(y)*x + x**3 - 1, x)) == 3
    assert len(solve(-512*y**3 + 1344*(x + 2)**Rational(1, 3)*y**2 -
        1176*(x + 2)**Rational(2, 3)*y - 169*x + 686, y, _unrad=False)) == 3

    # watch out for when the cov doesn't involve the symbol of interest
    eq = S('-x + (7*y/8 - (27*x/2 + 27*sqrt(x**2)/2)**(1/3)/3)**3 - 1')
    assert solve(eq, y) == [
        2**(S(2)/3)*(27*x + 27*sqrt(x**2))**(S(1)/3)*S(4)/21 + (512*x/343 +
        S(512)/343)**(S(1)/3)*(-S(1)/2 - sqrt(3)*I/2), 2**(S(2)/3)*(27*x +
        27*sqrt(x**2))**(S(1)/3)*S(4)/21 + (512*x/343 +
        S(512)/343)**(S(1)/3)*(-S(1)/2 + sqrt(3)*I/2), 2**(S(2)/3)*(27*x +
        27*sqrt(x**2))**(S(1)/3)*S(4)/21 + (512*x/343 + S(512)/343)**(S(1)/3)]

    eq = root(x + 1, 3) - (root(x, 3) + root(x, 5))
    assert check(unrad(eq),
        (3*s**13 + 3*s**11 + s**9 - 1, [s, s**15 - x]))
    assert check(unrad(eq - 2),
        (3*s**13 + 3*s**11 + 6*s**10 + s**9 + 12*s**8 + 6*s**6 + 12*s**5 +
        12*s**3 + 7, [s, s**15 - x]))
    assert check(unrad(root(x, 3) - root(x + 1, 4)/2 + root(x + 2, 3)),
        (s*(4096*s**9 + 960*s**8 + 48*s**7 - s**6 - 1728),
        [s, s**4 - x - 1]))  # orig expr has two real roots: -1, -.389
    assert check(unrad(root(x, 3) + root(x + 1, 4) - root(x + 2, 3)/2),
        (343*s**13 + 2904*s**12 + 1344*s**11 + 512*s**10 - 1323*s**9 -
        3024*s**8 - 1728*s**7 + 1701*s**5 + 216*s**4 - 729*s, [s, s**4 - x -
        1]))  # orig expr has one real root: -0.048
    assert check(unrad(root(x, 3)/2 - root(x + 1, 4) + root(x + 2, 3)),
        (729*s**13 - 216*s**12 + 1728*s**11 - 512*s**10 + 1701*s**9 -
        3024*s**8 + 1344*s**7 + 1323*s**5 - 2904*s**4 + 343*s, [s, s**4 - x -
        1]))  # orig expr has 2 real roots: -0.91, -0.15
    assert check(unrad(root(x, 3)/2 - root(x + 1, 4) + root(x + 2, 3) - 2),
        (729*s**13 + 1242*s**12 + 18496*s**10 + 129701*s**9 + 388602*s**8 +
        453312*s**7 - 612864*s**6 - 3337173*s**5 - 6332418*s**4 - 7134912*s**3
        - 5064768*s**2 - 2111913*s - 398034, [s, s**4 - x - 1]))
        # orig expr has 1 real root: 19.53

    ans = solve(sqrt(x) + sqrt(x + 1) -
                sqrt(1 - x) - sqrt(2 + x))
    assert len(ans) == 1 and NS(ans[0])[:4] == '0.73'
    # the fence optimization problem
    # https://github.com/sympy/sympy/issues/4793#issuecomment-36994519
    F = Symbol('F')
    eq = F - (2*x + 2*y + sqrt(x**2 + y**2))
    ans = F*Rational(2, 7) - sqrt(2)*F/14
    X = solve(eq, x, check=False)
    for xi in reversed(X):  # reverse since currently, ans is the 2nd one
        Y = solve((x*y).subs(x, xi).diff(y), y, simplify=False, check=False)
        if any((a - ans).expand().is_zero for a in Y):
            break
    else:
        assert None  # no answer was found
    assert solve(sqrt(x + 1) + root(x, 3) - 2) == S('''
        [(-11/(9*(47/54 + sqrt(93)/6)**(1/3)) + 1/3 + (47/54 +
        sqrt(93)/6)**(1/3))**3]''')
    assert solve(sqrt(sqrt(x + 1)) + x**Rational(1, 3) - 2) == S('''
        [(-sqrt(-2*(-1/16 + sqrt(6913)/16)**(1/3) + 6/(-1/16 +
        sqrt(6913)/16)**(1/3) + 17/2 + 121/(4*sqrt(-6/(-1/16 +
        sqrt(6913)/16)**(1/3) + 2*(-1/16 + sqrt(6913)/16)**(1/3) + 17/4)))/2 +
        sqrt(-6/(-1/16 + sqrt(6913)/16)**(1/3) + 2*(-1/16 +
        sqrt(6913)/16)**(1/3) + 17/4)/2 + 9/4)**3]''')
    assert solve(sqrt(x) + root(sqrt(x) + 1, 3) - 2) == S('''
        [(-(81/2 + 3*sqrt(741)/2)**(1/3)/3 + (81/2 + 3*sqrt(741)/2)**(-1/3) +
        2)**2]''')
    eq = S('''
        -x + (1/2 - sqrt(3)*I/2)*(3*x**3/2 - x*(3*x**2 - 34)/2 + sqrt((-3*x**3
        + x*(3*x**2 - 34) + 90)**2/4 - 39304/27) - 45)**(1/3) + 34/(3*(1/2 -
        sqrt(3)*I/2)*(3*x**3/2 - x*(3*x**2 - 34)/2 + sqrt((-3*x**3 + x*(3*x**2
        - 34) + 90)**2/4 - 39304/27) - 45)**(1/3))''')
    assert check(unrad(eq),
        (s*-(-s**6 + sqrt(3)*s**6*I - 153*2**Rational(2, 3)*3**Rational(1, 3)*s**4 +
        51*12**Rational(1, 3)*s**4 - 102*2**Rational(2, 3)*3**Rational(5, 6)*s**4*I - 1620*s**3 +
        1620*sqrt(3)*s**3*I + 13872*18**Rational(1, 3)*s**2 - 471648 +
        471648*sqrt(3)*I), [s, s**3 - 306*x - sqrt(3)*sqrt(31212*x**2 -
        165240*x + 61484) + 810]))

    assert solve(eq) == [] # not other code errors
    eq = root(x, 3) - root(y, 3) + root(x, 5)
    assert check(unrad(eq),
           (s**15 + 3*s**13 + 3*s**11 + s**9 - y, [s, s**15 - x]))
    eq = root(x, 3) + root(y, 3) + root(x*y, 4)
    assert check(unrad(eq),
                 (s*y*(-s**12 - 3*s**11*y - 3*s**10*y**2 - s**9*y**3 -
                       3*s**8*y**2 + 21*s**7*y**3 - 3*s**6*y**4 - 3*s**4*y**4 -
                       3*s**3*y**5 - y**6), [s, s**4 - x*y]))
    raises(NotImplementedError,
           lambda: unrad(root(x, 3) + root(y, 3) + root(x*y, 5)))

    # Test unrad with an Equality
    eq = Eq(-x**(S(1)/5) + x**(S(1)/3), -3**(S(1)/3) - (-1)**(S(3)/5)*3**(S(1)/5))
    assert check(unrad(eq),
        (-s**5 + s**3 - 3**(S(1)/3) - (-1)**(S(3)/5)*3**(S(1)/5), [s, s**15 - x]))

    # make sure buried radicals are exposed
    s = sqrt(x) - 1
    assert unrad(s**2 - s**3) == (x**3 - 6*x**2 + 9*x - 4, [])
    # make sure numerators which are already polynomial are rejected
    assert unrad((x/(x + 1) + 3)**(-2), x) is None

    # https://github.com/sympy/sympy/issues/23707
    eq = sqrt(x - y)*exp(t*sqrt(x - y)) - exp(t*sqrt(x - y))
    assert solve(eq, y) == [x - 1]
    assert unrad(eq) is None

