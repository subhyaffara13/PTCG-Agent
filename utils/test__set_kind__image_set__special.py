
def test_SetKind_ImageSet_Special():
    f = ImageSet(Lambda(n, n ** 2), Interval(1, 4))
    assert (f - FiniteSet(3)).kind is SetKind(NumberKind)
    assert (f + Interval(16, 17)).kind is SetKind(NumberKind)
    assert (f + FiniteSet(17)).kind is SetKind(NumberKind)

