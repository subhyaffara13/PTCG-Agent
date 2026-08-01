
def test_Eq():
    assert Eq(Interval(0, 1), Interval(0, 1))
    assert Eq(Interval(0, 1), Interval(0, 2)) == False

    s1 = FiniteSet(0, 1)
    s2 = FiniteSet(1, 2)

    assert Eq(s1, s1)
    assert Eq(s1, s2) == False

    assert Eq(s1*s2, s1*s2)
    assert Eq(s1*s2, s2*s1) == False

    assert unchanged(Eq, FiniteSet({x, y}), FiniteSet({x}))
    assert Eq(FiniteSet({x, y}).subs(y, x), FiniteSet({x})) is S.true
    assert Eq(FiniteSet({x, y}), FiniteSet({x})).subs(y, x) is S.true
    assert Eq(FiniteSet({x, y}).subs(y, x+1), FiniteSet({x})) is S.false
    assert Eq(FiniteSet({x, y}), FiniteSet({x})).subs(y, x+1) is S.false

    assert Eq(ProductSet({1}, {2}), Interval(1, 2)) is S.false
    assert Eq(ProductSet({1}), ProductSet({1}, {2})) is S.false

    assert Eq(FiniteSet(()), FiniteSet(1)) is S.false
    assert Eq(ProductSet(), FiniteSet(1)) is S.false

    i1 = Interval(0, 1)
    i2 = Interval(x, y)
    assert unchanged(Eq, ProductSet(i1, i1), ProductSet(i2, i2))

