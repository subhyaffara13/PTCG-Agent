
def test_issue_10401():
    x = symbols('x')
    fin = symbols('inf', finite=True)
    inf = symbols('inf', infinite=True)
    inf2 = symbols('inf2', infinite=True)
    infx = symbols('infx', infinite=True, extended_real=True)
    # Used in the commented tests below:
    #infx2 = symbols('infx2', infinite=True, extended_real=True)
    infnx = symbols('inf~x', infinite=True, extended_real=False)
    infnx2 = symbols('inf~x2', infinite=True, extended_real=False)
    infp = symbols('infp', infinite=True, extended_positive=True)
    infp1 = symbols('infp1', infinite=True, extended_positive=True)
    infn = symbols('infn', infinite=True, extended_negative=True)
    zero = symbols('z', zero=True)
    nonzero = symbols('nz', zero=False, finite=True)

    assert Eq(1/(1/x + 1), 1).func is Eq
    assert Eq(1/(1/x + 1), 1).subs(x, S.ComplexInfinity) is S.true
    assert Eq(1/(1/fin + 1), 1) is S.false

    T, F = S.true, S.false
    assert Eq(fin, inf) is F
    assert Eq(inf, inf2) not in (T, F) and inf != inf2
    assert Eq(1 + inf, 2 + inf2) not in (T, F) and inf != inf2
    assert Eq(infp, infp1) is T
    assert Eq(infp, infn) is F
    assert Eq(1 + I*oo, I*oo) is F
    assert Eq(I*oo, 1 + I*oo) is F
    assert Eq(1 + I*oo, 2 + I*oo) is F
    assert Eq(1 + I*oo, 2 + I*infx) is F
    assert Eq(1 + I*oo, 2 + infx) is F
    # FIXME: The test below fails because (-infx).is_extended_positive is True
    # (should be None)
    #assert Eq(1 + I*infx, 1 + I*infx2) not in (T, F) and infx != infx2
    #
    assert Eq(zoo, sqrt(2) + I*oo) is F
    assert Eq(zoo, oo) is F
    r = Symbol('r', real=True)
    i = Symbol('i', imaginary=True)
    assert Eq(i*I, r) not in (T, F)
    assert Eq(infx, infnx) is F
    assert Eq(infnx, infnx2) not in (T, F) and infnx != infnx2
    assert Eq(zoo, oo) is F
    assert Eq(inf/inf2, 0) is F
    assert Eq(inf/fin, 0) is F
    assert Eq(fin/inf, 0) is T
    assert Eq(zero/nonzero, 0) is T and ((zero/nonzero) != 0)
    # The commented out test below is incorrect because:
    assert zoo == -zoo
    assert Eq(zoo, -zoo) is T
    assert Eq(oo, -oo) is F
    assert Eq(inf, -inf) not in (T, F)

    assert Eq(fin/(fin + 1), 1) is S.false

    o = symbols('o', odd=True)
    assert Eq(o, 2*o) is S.false

    p = symbols('p', positive=True)
    assert Eq(p/(p - 1), 1) is F

