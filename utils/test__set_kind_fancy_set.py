
def test_SetKind_fancySet():
    G = lambda *args: ImageSet(Lambda(x, x ** 2), *args)
    assert G(Interval(1, 4)).kind is SetKind(NumberKind)
    assert G(FiniteSet(1, 4)).kind is SetKind(NumberKind)
    assert S.Rationals.kind is SetKind(NumberKind)
    assert S.Naturals.kind is SetKind(NumberKind)
    assert S.Integers.kind is SetKind(NumberKind)
    assert Range(3).kind is SetKind(NumberKind)
    a = Interval(2, 3)
    b = Interval(4, 6)
    c1 = ComplexRegion(a*b)
    assert c1.kind is SetKind(TupleKind(NumberKind, NumberKind))

