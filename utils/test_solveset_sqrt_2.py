
def test_solveset_sqrt_2():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    # http://tutorial.math.lamar.edu/Classes/Alg/SolveRadicalEqns.aspx#Solve_Rad_Ex2_a
    assert solveset_real(sqrt(2*x - 1) - sqrt(x - 4) - 2, x) == \
        FiniteSet(S(5), S(13))
    assert solveset_real(sqrt(x + 7) + 2 - sqrt(3 - x), x) == \
        FiniteSet(-6)

    # http://www.purplemath.com/modules/solverad.htm
    assert solveset_real(sqrt(17*x - sqrt(x**2 - 5)) - 7, x) == \
        FiniteSet(3)

    eq = x + 1 - (x**4 + 4*x**3 - x)**Rational(1, 4)
    assert solveset_real(eq, x) == FiniteSet(Rational(-1, 2), Rational(-1, 3))

    eq = sqrt(2*x + 9) - sqrt(x + 1) - sqrt(x + 4)
    assert solveset_real(eq, x) == FiniteSet(0)

    eq = sqrt(x + 4) + sqrt(2*x - 1) - 3*sqrt(x - 1)
    assert solveset_real(eq, x) == FiniteSet(5)

    eq = sqrt(x)*sqrt(x - 7) - 12
    assert solveset_real(eq, x) == FiniteSet(16)

    eq = sqrt(x - 3) + sqrt(x) - 3
    assert solveset_real(eq, x) == FiniteSet(4)

    eq = sqrt(2*x**2 - 7) - (3 - x)
    assert solveset_real(eq, x) == FiniteSet(-S(8), S(2))

    # others
    eq = sqrt(9*x**2 + 4) - (3*x + 2)
    assert solveset_real(eq, x) == FiniteSet(0)

    assert solveset_real(sqrt(x - 3) - sqrt(x) - 3, x) == FiniteSet()

    eq = (2*x - 5)**Rational(1, 3) - 3
    assert solveset_real(eq, x) == FiniteSet(16)

    assert solveset_real(sqrt(x) + sqrt(sqrt(x)) - 4, x) == \
        FiniteSet((Rational(-1, 2) + sqrt(17)/2)**4)

    eq = sqrt(x) - sqrt(x - 1) + sqrt(sqrt(x))
    assert solveset_real(eq, x) == FiniteSet()

    eq = (x - 4)**2 + (sqrt(x) - 2)**4
    assert solveset_real(eq, x) == FiniteSet(-4, 4)

    eq = (sqrt(x) + sqrt(x + 1) + sqrt(1 - x) - 6*sqrt(5)/5)
    ans = solveset_real(eq, x)
    ra = S('''-1484/375 - 4*(-S(1)/2 + sqrt(3)*I/2)*(-12459439/52734375 +
    114*sqrt(12657)/78125)**(S(1)/3) - 172564/(140625*(-S(1)/2 +
    sqrt(3)*I/2)*(-12459439/52734375 + 114*sqrt(12657)/78125)**(S(1)/3))''')
    rb = Rational(4, 5)
    assert all(abs(eq.subs(x, i).n()) < 1e-10 for i in (ra, rb)) and \
        len(ans) == 2 and \
        {i.n(chop=True) for i in ans} == \
        {i.n(chop=True) for i in (ra, rb)}

    assert solveset_real(sqrt(x) + x**Rational(1, 3) +
                                 x**Rational(1, 4), x) == FiniteSet(0)

    assert solveset_real(x/sqrt(x**2 + 1), x) == FiniteSet(0)

    eq = (x - y**3)/((y**2)*sqrt(1 - y**2))
    assert solveset_real(eq, x) == FiniteSet(y**3)

    # issue 4497
    assert solveset_real(1/(5 + x)**Rational(1, 5) - 9, x) == \
        FiniteSet(Rational(-295244, 59049))

