
def test_subs_CondSet():
    s = FiniteSet(z, y)
    c = ConditionSet(x, x < 2, s)
    assert c.subs(x, y) == c
    assert c.subs(z, y) == ConditionSet(x, x < 2, FiniteSet(y))
    assert c.xreplace({x: y}) == ConditionSet(y, y < 2, s)

    assert ConditionSet(x, x < y, s
        ).subs(y, w) == ConditionSet(x, x < w, s.subs(y, w))
    # if the user uses assumptions that cause the condition
    # to evaluate, that can't be helped from SymPy's end
    n = Symbol('n', negative=True)
    assert ConditionSet(n, 0 < n, S.Integers) is S.EmptySet
    p = Symbol('p', positive=True)
    assert ConditionSet(n, n < y, S.Integers
        ).subs(n, x) == ConditionSet(n, n < y, S.Integers)
    raises(ValueError, lambda: ConditionSet(
        x + 1, x < 1, S.Integers))
    assert ConditionSet(
        p, n < x, Interval(-5, 5)).subs(x, p) == Interval(-5, 5), ConditionSet(
        p, n < x, Interval(-5, 5)).subs(x, p)
    assert ConditionSet(
        n, n < x, Interval(-oo, 0)).subs(x, p
        ) == Interval(-oo, 0)

    assert ConditionSet(f(x), f(x) < 1, {w, z}
        ).subs(f(x), y) == ConditionSet(f(x), f(x) < 1, {w, z})

    # issue 17341
    k = Symbol('k')
    img1 = ImageSet(Lambda(k, 2*k*pi + asin(y)), S.Integers)
    img2 = ImageSet(Lambda(k, 2*k*pi + asin(S.One/3)), S.Integers)
    assert ConditionSet(x, Contains(
        y, Interval(-1,1)), img1).subs(y, S.One/3).dummy_eq(img2)

    assert (0, 1) in ConditionSet((x, y), x + y < 3, S.Integers**2)

    raises(TypeError, lambda: ConditionSet(n, n < -10, Interval(0, 10)))

