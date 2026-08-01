
def test_dummy_eq():
    C = ConditionSet
    I = S.Integers
    c = C(x, x < 1, I)
    assert c.dummy_eq(C(y, y < 1, I))
    assert c.dummy_eq(1) == False
    assert c.dummy_eq(C(x, x < 1, S.Reals)) == False

    c1 = ConditionSet((x, y), Eq(x + 1, 0) & Eq(x + y, 0), S.Reals**2)
    c2 = ConditionSet((x, y), Eq(x + 1, 0) & Eq(x + y, 0), S.Reals**2)
    c3 = ConditionSet((x, y), Eq(x + 1, 0) & Eq(x + y, 0), S.Complexes**2)
    assert c1.dummy_eq(c2)
    assert c1.dummy_eq(c3) is False
    assert c.dummy_eq(c1) is False
    assert c1.dummy_eq(c) is False

    # issue 19496
    m = Symbol('m')
    n = Symbol('n')
    a = Symbol('a')
    d1 = ImageSet(Lambda(m, m*pi), S.Integers)
    d2 = ImageSet(Lambda(n, n*pi), S.Integers)
    c1 = ConditionSet(x, Ne(a, 0), d1)
    c2 = ConditionSet(x, Ne(a, 0), d2)
    assert c1.dummy_eq(c2)


def test_dummy_eq():
    x = Symbol('x')
    y = Symbol('y')

    u = Dummy('u')

    assert (u**2 + 1).dummy_eq(x**2 + 1) is True
    assert ((u**2 + 1) == (x**2 + 1)) is False

    assert (u**2 + y).dummy_eq(x**2 + y, x) is True
    assert (u**2 + y).dummy_eq(x**2 + y, y) is False

