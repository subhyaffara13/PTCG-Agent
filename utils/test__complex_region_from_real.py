
def test_ComplexRegion_from_real():
    c1 = ComplexRegion(Interval(0, 1) * Interval(0, 2 * S.Pi), polar=True)

    raises(ValueError, lambda: c1.from_real(c1))
    assert c1.from_real(Interval(-1, 1)) == ComplexRegion(Interval(-1, 1) * FiniteSet(0), False)

