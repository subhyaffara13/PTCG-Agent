
def test_integer_domain_relational_isolve():

    dom = FiniteSet(0, 3)
    x = Symbol('x',zero=False)
    assert isolve((x - 1)*(x - 2)*(x - 4) < 0, x, domain=dom) == Eq(x, 3)

    x = Symbol('x')
    assert isolve(x + 2 < 0, x, domain=S.Integers) == \
           (x <= -3) & (x > -oo) & Eq(Mod(x, 1), 0)
    assert isolve(2 * x + 3 > 0, x, domain=S.Integers) == \
           (x >= -1) & (x < oo)  & Eq(Mod(x, 1), 0)
    assert isolve((x ** 2 + 3 * x - 2) < 0, x, domain=S.Integers) == \
           (x >= -3) & (x <= 0)  & Eq(Mod(x, 1), 0)
    assert isolve((x ** 2 + 3 * x - 2) > 0, x, domain=S.Integers) == \
           ((x >= 1) & (x < oo)  & Eq(Mod(x, 1), 0)) | (
               (x <= -4) & (x > -oo)  & Eq(Mod(x, 1), 0))

