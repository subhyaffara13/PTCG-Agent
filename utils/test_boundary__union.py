
def test_boundary_Union():
    assert (Interval(0, 1) + Interval(2, 3)).boundary == FiniteSet(0, 1, 2, 3)
    assert ((Interval(0, 1, False, True)
           + Interval(1, 2, True, False)).boundary == FiniteSet(0, 1, 2))

    assert (Interval(0, 1) + FiniteSet(2)).boundary == FiniteSet(0, 1, 2)
    assert Union(Interval(0, 10), Interval(5, 15), evaluate=False).boundary \
            == FiniteSet(0, 15)

    assert Union(Interval(0, 10), Interval(0, 1), evaluate=False).boundary \
            == FiniteSet(0, 10)
    assert Union(Interval(0, 10, True, True),
                 Interval(10, 15, True, True), evaluate=False).boundary \
            == FiniteSet(0, 10, 15)

