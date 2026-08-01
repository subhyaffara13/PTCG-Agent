
def test_atan2():
    assert solve(atan2(x, 2) - pi/3, x) == [2*sqrt(3)]


def test_atan2():
    # The .inverse() method on atan2 works only if x.is_real is True and the
    # second argument is a real constant
    assert solveset_real(atan2(x, 2) - pi/3, x) == FiniteSet(2*sqrt(3))


def test_atan2():
    assert atan2.nargs == FiniteSet(2)
    assert atan2(0, 0) is S.NaN
    assert atan2(0, 1) == 0
    assert atan2(1, 1) == pi/4
    assert atan2(1, 0) == pi/2
    assert atan2(1, -1) == pi*Rational(3, 4)
    assert atan2(0, -1) == pi
    assert atan2(-1, -1) == pi*Rational(-3, 4)
    assert atan2(-1, 0) == -pi/2
    assert atan2(-1, 1) == -pi/4
    i = symbols('i', imaginary=True)
    r = symbols('r', real=True)
    eq = atan2(r, i)
    ans = -I*log((i + I*r)/sqrt(i**2 + r**2))
    reps = ((r, 2), (i, I))
    assert eq.subs(reps) == ans.subs(reps)

    x = Symbol('x', negative=True)
    y = Symbol('y', negative=True)
    assert atan2(y, x) == atan(y/x) - pi
    y = Symbol('y', nonnegative=True)
    assert atan2(y, x) == atan(y/x) + pi
    y = Symbol('y')
    assert atan2(y, x) == atan2(y, x, evaluate=False)

    u = Symbol("u", positive=True)
    assert atan2(0, u) == 0
    u = Symbol("u", negative=True)
    assert atan2(0, u) == pi

    assert atan2(y, oo) ==  0
    assert atan2(y, -oo)==  2*pi*Heaviside(re(y), S.Half) - pi

    assert atan2(y, x).rewrite(log) == -I*log((x + I*y)/sqrt(x**2 + y**2))
    assert atan2(0, 0) is S.NaN

    ex = atan2(y, x) - arg(x + I*y)
    assert ex.subs({x:2, y:3}).rewrite(arg) == 0
    assert ex.subs({x:2, y:3*I}).rewrite(arg) == -pi - I*log(sqrt(5)*I/5)
    assert ex.subs({x:2*I, y:3}).rewrite(arg) == -pi/2 - I*log(sqrt(5)*I)
    assert ex.subs({x:2*I, y:3*I}).rewrite(arg) == -pi + atan(Rational(2, 3)) + atan(Rational(3, 2))
    i = symbols('i', imaginary=True)
    r = symbols('r', real=True)
    e = atan2(i, r)
    rewrite = e.rewrite(arg)
    reps = {i: I, r: -2}
    assert rewrite == -I*log(abs(I*i + r)/sqrt(abs(i**2 + r**2))) + arg((I*i + r)/sqrt(i**2 + r**2))
    assert (e - rewrite).subs(reps).equals(0)

    assert atan2(0, x).rewrite(atan) == Piecewise((pi, re(x) < 0),
                                            (0, Ne(x, 0)),
                                            (nan, True))
    assert atan2(0, r).rewrite(atan) == Piecewise((pi, r < 0), (0, Ne(r, 0)), (S.NaN, True))
    assert atan2(0, i),rewrite(atan) == 0
    assert atan2(0, r + i).rewrite(atan) == Piecewise((pi, r < 0), (0, True))

    assert atan2(y, x).rewrite(atan) == Piecewise(
            (2*atan(y/(x + sqrt(x**2 + y**2))), Ne(y, 0)),
            (pi, re(x) < 0),
            (0, (re(x) > 0) | Ne(im(x), 0)),
            (nan, True))
    assert conjugate(atan2(x, y)) == atan2(conjugate(x), conjugate(y))

    assert diff(atan2(y, x), x) == -y/(x**2 + y**2)
    assert diff(atan2(y, x), y) == x/(x**2 + y**2)

    assert simplify(diff(atan2(y, x).rewrite(log), x)) == -y/(x**2 + y**2)
    assert simplify(diff(atan2(y, x).rewrite(log), y)) ==  x/(x**2 + y**2)

    assert str(atan2(1, 2).evalf(5)) == '0.46365'
    raises(ArgumentIndexError, lambda: atan2(x, y).fdiff(3))


def test_atan2():
    assert refine(atan2(y, x), Q.real(y) & Q.positive(x)) == atan(y/x)
    assert refine(atan2(y, x), Q.negative(y) & Q.positive(x)) == atan(y/x)
    assert refine(atan2(y, x), Q.negative(y) & Q.negative(x)) == atan(y/x) - pi
    assert refine(atan2(y, x), Q.positive(y) & Q.negative(x)) == atan(y/x) + pi
    assert refine(atan2(y, x), Q.zero(y) & Q.negative(x)) == pi
    assert refine(atan2(y, x), Q.positive(y) & Q.zero(x)) == pi/2
    assert refine(atan2(y, x), Q.negative(y) & Q.zero(x)) == -pi/2
    assert refine(atan2(y, x), Q.zero(y) & Q.zero(x)) is nan


def test_atan2():
    mp.dps = 15
    assert atan2(1,1).ae(pi/4)
    assert atan2(1,-1).ae(3*pi/4)
    assert atan2(-1,-1).ae(-3*pi/4)
    assert atan2(-1,1).ae(-pi/4)
    assert atan2(-1,0).ae(-pi/2)
    assert atan2(1,0).ae(pi/2)
    assert atan2(0,0) == 0
    assert atan2(inf,0).ae(pi/2)
    assert atan2(-inf,0).ae(-pi/2)
    assert isnan(atan2(inf,inf))
    assert isnan(atan2(-inf,inf))
    assert isnan(atan2(inf,-inf))
    assert isnan(atan2(3,nan))
    assert isnan(atan2(nan,3))
    assert isnan(atan2(0,nan))
    assert isnan(atan2(nan,0))
    assert atan2(0,inf) == 0
    assert atan2(0,-inf).ae(pi)
    assert atan2(10,inf) == 0
    assert atan2(-10,inf) == 0
    assert atan2(-10,-inf).ae(-pi)
    assert atan2(10,-inf).ae(pi)
    assert atan2(inf,10).ae(pi/2)
    assert atan2(inf,-10).ae(pi/2)
    assert atan2(-inf,10).ae(-pi/2)
    assert atan2(-inf,-10).ae(-pi/2)

