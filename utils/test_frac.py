
def test_frac():
    assert limit(frac(x), x, oo) == AccumBounds(0, 1)
    assert limit(frac(x)**(1/x), x, oo) == AccumBounds(0, 1)
    assert limit(frac(x)**(1/x), x, -oo) == AccumBounds(1, oo)
    assert limit(frac(x)**x, x, oo) == AccumBounds(0, oo)  # wolfram gives (0, 1)
    assert limit(frac(sin(x)), x, 0, "+") == 0
    assert limit(frac(sin(x)), x, 0, "-") == 1
    assert limit(frac(cos(x)), x, 0, "+-") == 1
    assert limit(frac(x**2), x, 0, "+-") == 0
    raises(ValueError, lambda: limit(frac(x), x, 0, '+-'))
    assert limit(frac(-2*x + 1), x, 0, "+") == 1
    assert limit(frac(-2*x + 1), x, 0, "-") == 0
    assert limit(frac(x + S.Half), x, 0, "+-") == S(1)/2
    assert limit(frac(1/x), x, 0) == AccumBounds(0, 1)


def test_frac():
    assert frac(x).series(x, cdir=1) == x
    assert frac(x).series(x, cdir=-1) == 1 + x
    assert frac(2*x + 1).series(x, cdir=1) == 2*x
    assert frac(2*x + 1).series(x, cdir=-1) == 1 + 2*x
    assert frac(x**2).series(x, cdir=1) == x**2
    assert frac(x**2).series(x, cdir=-1) == x**2
    assert frac(sin(x) + 5).series(x, cdir=1) == x - x**3/6 + x**5/120 + O(x**6)
    assert frac(sin(x) + 5).series(x, cdir=-1) == 1 + x - x**3/6 + x**5/120 + O(x**6)
    assert frac(sin(x) + S.Half).series(x) == S.Half + x - x**3/6 + x**5/120 + O(x**6)
    assert frac(x**8).series(x, cdir=1) == O(x**6)
    assert frac(1/x).series(x) == AccumBounds(0, 1) + O(x**6)


def test_frac():
    from sympy.functions.elementary.integers import frac

    expr = frac(x)
    prntr = NumPyPrinter()
    assert prntr.doprint(expr) == 'numpy.mod(x, 1)'

    prntr = SciPyPrinter()
    assert prntr.doprint(expr) == 'numpy.mod(x, 1)'

    prntr = PythonCodePrinter()
    assert prntr.doprint(expr) == 'x % 1'

    prntr = MpmathPrinter()
    assert prntr.doprint(expr) == 'mpmath.frac(x)'

    prntr = SymPyPrinter()
    assert prntr.doprint(expr) == 'sympy.functions.elementary.integers.frac(x)'


def test_frac():
    assert isinstance(frac(x), frac)
    assert frac(oo) == AccumBounds(0, 1)
    assert frac(-oo) == AccumBounds(0, 1)
    assert frac(zoo) is nan

    assert frac(n) == 0
    assert frac(nan) is nan
    assert frac(Rational(4, 3)) == Rational(1, 3)
    assert frac(-Rational(4, 3)) == Rational(2, 3)
    assert frac(Rational(-4, 3)) == Rational(2, 3)

    r = Symbol('r', real=True)
    assert frac(I*r) == I*frac(r)
    assert frac(1 + I*r) == I*frac(r)
    assert frac(0.5 + I*r) == 0.5 + I*frac(r)
    assert frac(n + I*r) == I*frac(r)
    assert frac(n + I*k) == 0
    assert unchanged(frac, x + I*x)
    assert frac(x + I*n) == frac(x)

    assert frac(x).rewrite(floor) == x - floor(x)
    assert frac(x).rewrite(ceiling) == x + ceiling(-x)
    assert frac(y).rewrite(floor).subs(y, pi) == frac(pi)
    assert frac(y).rewrite(floor).subs(y, -E) == frac(-E)
    assert frac(y).rewrite(ceiling).subs(y, -pi) == frac(-pi)
    assert frac(y).rewrite(ceiling).subs(y, E) == frac(E)

    assert Eq(frac(y), y - floor(y))
    assert Eq(frac(y), y + ceiling(-y))

    r = Symbol('r', real=True)
    p_i = Symbol('p_i', integer=True, positive=True)
    n_i = Symbol('p_i', integer=True, negative=True)
    np_i = Symbol('np_i', integer=True, nonpositive=True)
    nn_i = Symbol('nn_i', integer=True, nonnegative=True)
    p_r = Symbol('p_r', positive=True)
    n_r = Symbol('n_r', negative=True)
    np_r = Symbol('np_r', real=True, nonpositive=True)
    nn_r = Symbol('nn_r', real=True, nonnegative=True)

    # Real frac argument, integer rhs
    assert frac(r) <= p_i
    assert not frac(r) <= n_i
    assert (frac(r) <= np_i).has(Le)
    assert (frac(r) <= nn_i).has(Le)
    assert frac(r) < p_i
    assert not frac(r) < n_i
    assert not frac(r) < np_i
    assert (frac(r) < nn_i).has(Lt)
    assert not frac(r) >= p_i
    assert frac(r) >= n_i
    assert frac(r) >= np_i
    assert (frac(r) >= nn_i).has(Ge)
    assert not frac(r) > p_i
    assert frac(r) > n_i
    assert (frac(r) > np_i).has(Gt)
    assert (frac(r) > nn_i).has(Gt)

    assert not Eq(frac(r), p_i)
    assert not Eq(frac(r), n_i)
    assert Eq(frac(r), np_i).has(Eq)
    assert Eq(frac(r), nn_i).has(Eq)

    assert Ne(frac(r), p_i)
    assert Ne(frac(r), n_i)
    assert Ne(frac(r), np_i).has(Ne)
    assert Ne(frac(r), nn_i).has(Ne)


    # Real frac argument, real rhs
    assert (frac(r) <= p_r).has(Le)
    assert not frac(r) <= n_r
    assert (frac(r) <= np_r).has(Le)
    assert (frac(r) <= nn_r).has(Le)
    assert (frac(r) < p_r).has(Lt)
    assert not frac(r) < n_r
    assert not frac(r) < np_r
    assert (frac(r) < nn_r).has(Lt)
    assert (frac(r) >= p_r).has(Ge)
    assert frac(r) >= n_r
    assert frac(r) >= np_r
    assert (frac(r) >= nn_r).has(Ge)
    assert (frac(r) > p_r).has(Gt)
    assert frac(r) > n_r
    assert (frac(r) > np_r).has(Gt)
    assert (frac(r) > nn_r).has(Gt)

    assert not Eq(frac(r), n_r)
    assert Eq(frac(r), p_r).has(Eq)
    assert Eq(frac(r), np_r).has(Eq)
    assert Eq(frac(r), nn_r).has(Eq)

    assert Ne(frac(r), p_r).has(Ne)
    assert Ne(frac(r), n_r)
    assert Ne(frac(r), np_r).has(Ne)
    assert Ne(frac(r), nn_r).has(Ne)

    # Real frac argument, +/- oo rhs
    assert frac(r) < oo
    assert frac(r) <= oo
    assert not frac(r) > oo
    assert not frac(r) >= oo

    assert not frac(r) < -oo
    assert not frac(r) <= -oo
    assert frac(r) > -oo
    assert frac(r) >= -oo

    assert frac(r) < 1
    assert frac(r) <= 1
    assert not frac(r) > 1
    assert not frac(r) >= 1

    assert not frac(r) < 0
    assert (frac(r) <= 0).has(Le)
    assert (frac(r) > 0).has(Gt)
    assert frac(r) >= 0

    # Some test for numbers
    assert frac(r) <= sqrt(2)
    assert (frac(r) <= sqrt(3) - sqrt(2)).has(Le)
    assert not frac(r) <= sqrt(2) - sqrt(3)
    assert not frac(r) >= sqrt(2)
    assert (frac(r) >= sqrt(3) - sqrt(2)).has(Ge)
    assert frac(r) >= sqrt(2) - sqrt(3)

    assert not Eq(frac(r), sqrt(2))
    assert Eq(frac(r), sqrt(3) - sqrt(2)).has(Eq)
    assert not Eq(frac(r), sqrt(2) - sqrt(3))
    assert Ne(frac(r), sqrt(2))
    assert Ne(frac(r), sqrt(3) - sqrt(2)).has(Ne)
    assert Ne(frac(r), sqrt(2) - sqrt(3))

    assert frac(p_i, evaluate=False).is_zero
    assert frac(p_i, evaluate=False).is_finite
    assert frac(p_i, evaluate=False).is_integer
    assert frac(p_i, evaluate=False).is_real
    assert frac(r).is_finite
    assert frac(r).is_real
    assert frac(r).is_zero is None
    assert frac(r).is_integer is None

    assert frac(oo).is_finite
    assert frac(oo).is_real

