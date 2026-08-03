from typing import Union

def test_ComplexRegion_union():
    # Polar form
    c1 = ComplexRegion(Interval(0, 1)*Interval(0, 2*S.Pi), polar=True)
    c2 = ComplexRegion(Interval(0, 1)*Interval(0, S.Pi), polar=True)
    c3 = ComplexRegion(Interval(0, oo)*Interval(0, S.Pi), polar=True)
    c4 = ComplexRegion(Interval(0, oo)*Interval(S.Pi, 2*S.Pi), polar=True)

    p1 = Union(Interval(0, 1)*Interval(0, 2*S.Pi), Interval(0, 1)*Interval(0, S.Pi))
    p2 = Union(Interval(0, oo)*Interval(0, S.Pi), Interval(0, oo)*Interval(S.Pi, 2*S.Pi))

    assert c1.union(c2) == ComplexRegion(p1, polar=True)
    assert c3.union(c4) == ComplexRegion(p2, polar=True)

    # Rectangular form
    c5 = ComplexRegion(Interval(2, 5)*Interval(6, 9))
    c6 = ComplexRegion(Interval(4, 6)*Interval(10, 12))
    c7 = ComplexRegion(Interval(0, 10)*Interval(-10, 0))
    c8 = ComplexRegion(Interval(12, 16)*Interval(14, 20))

    p3 = Union(Interval(2, 5)*Interval(6, 9), Interval(4, 6)*Interval(10, 12))
    p4 = Union(Interval(0, 10)*Interval(-10, 0), Interval(12, 16)*Interval(14, 20))

    assert c5.union(c6) == ComplexRegion(p3)
    assert c7.union(c8) == ComplexRegion(p4)

    assert c1.union(Interval(2, 4)) == Union(c1, Interval(2, 4), evaluate=False)
    assert c5.union(Interval(2, 4)) == Union(c5, ComplexRegion.from_real(Interval(2, 4)))

