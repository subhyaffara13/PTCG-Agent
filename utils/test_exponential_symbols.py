
def test_exponential_symbols():
    x, y, z = symbols('x y z', positive=True)
    xr, zr = symbols('xr, zr', real=True)

    assert solveset(z**x - y, x, S.Reals) == Intersection(
        S.Reals, FiniteSet(log(y)/log(z)))

    f1 = 2*x**w - 4*y**w
    f2 = (x/y)**w - 2
    sol1 = Intersection({log(2)/(log(x) - log(y))}, S.Reals)
    sol2 = Intersection({log(2)/log(x/y)}, S.Reals)
    assert solveset(f1, w, S.Reals) == sol1, solveset(f1, w, S.Reals)
    assert solveset(f2, w, S.Reals) == sol2, solveset(f2, w, S.Reals)

    assert solveset(x**x, x, Interval.Lopen(0,oo)).dummy_eq(
        ConditionSet(w, Eq(w**w, 0), Interval.open(0, oo)))
    assert solveset(x**y - 1, y, S.Reals) == FiniteSet(0)
    assert solveset(exp(x/y)*exp(-z/y) - 2, y, S.Reals) == \
    Complement(ConditionSet(y, Eq(im(x)/y, 0) & Eq(im(z)/y, 0), \
    Complement(Intersection(FiniteSet((x - z)/log(2)), S.Reals), FiniteSet(0))), FiniteSet(0))
    assert solveset(exp(xr/y)*exp(-zr/y) - 2, y, S.Reals) == \
        Complement(FiniteSet((xr - zr)/log(2)), FiniteSet(0))

    assert solveset(a**x - b**x, x).dummy_eq(ConditionSet(
        w, Ne(a, 0) & Ne(b, 0), FiniteSet(0)))

