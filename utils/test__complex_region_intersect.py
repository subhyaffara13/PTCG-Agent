
def test_ComplexRegion_intersect():
    # Polar form
    X_axis = ComplexRegion(Interval(0, oo)*FiniteSet(0, S.Pi), polar=True)

    unit_disk = ComplexRegion(Interval(0, 1)*Interval(0, 2*S.Pi), polar=True)
    upper_half_unit_disk = ComplexRegion(Interval(0, 1)*Interval(0, S.Pi), polar=True)
    upper_half_disk = ComplexRegion(Interval(0, oo)*Interval(0, S.Pi), polar=True)
    lower_half_disk = ComplexRegion(Interval(0, oo)*Interval(S.Pi, 2*S.Pi), polar=True)
    right_half_disk = ComplexRegion(Interval(0, oo)*Interval(-S.Pi/2, S.Pi/2), polar=True)
    first_quad_disk = ComplexRegion(Interval(0, oo)*Interval(0, S.Pi/2), polar=True)

    assert upper_half_disk.intersect(unit_disk) == upper_half_unit_disk
    assert right_half_disk.intersect(first_quad_disk) == first_quad_disk
    assert upper_half_disk.intersect(right_half_disk) == first_quad_disk
    assert upper_half_disk.intersect(lower_half_disk) == X_axis

    c1 = ComplexRegion(Interval(0, 4)*Interval(0, 2*S.Pi), polar=True)
    assert c1.intersect(Interval(1, 5)) == Interval(1, 4)
    assert c1.intersect(Interval(4, 9)) == FiniteSet(4)
    assert c1.intersect(Interval(5, 12)) is S.EmptySet

    # Rectangular form
    X_axis = ComplexRegion(Interval(-oo, oo)*FiniteSet(0))

    unit_square = ComplexRegion(Interval(-1, 1)*Interval(-1, 1))
    upper_half_unit_square = ComplexRegion(Interval(-1, 1)*Interval(0, 1))
    upper_half_plane = ComplexRegion(Interval(-oo, oo)*Interval(0, oo))
    lower_half_plane = ComplexRegion(Interval(-oo, oo)*Interval(-oo, 0))
    right_half_plane = ComplexRegion(Interval(0, oo)*Interval(-oo, oo))
    first_quad_plane = ComplexRegion(Interval(0, oo)*Interval(0, oo))

    assert upper_half_plane.intersect(unit_square) == upper_half_unit_square
    assert right_half_plane.intersect(first_quad_plane) == first_quad_plane
    assert upper_half_plane.intersect(right_half_plane) == first_quad_plane
    assert upper_half_plane.intersect(lower_half_plane) == X_axis

    c1 = ComplexRegion(Interval(-5, 5)*Interval(-10, 10))
    assert c1.intersect(Interval(2, 7)) == Interval(2, 5)
    assert c1.intersect(Interval(5, 7)) == FiniteSet(5)
    assert c1.intersect(Interval(6, 9)) is S.EmptySet

    # unevaluated object
    C1 = ComplexRegion(Interval(0, 1)*Interval(0, 2*S.Pi), polar=True)
    C2 = ComplexRegion(Interval(-1, 1)*Interval(-1, 1))
    assert C1.intersect(C2) == Intersection(C1, C2, evaluate=False)

