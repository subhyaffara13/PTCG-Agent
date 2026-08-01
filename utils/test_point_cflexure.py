
def test_point_cflexure():
    E = Symbol('E')
    I = Symbol('I')
    b = Beam(10, E, I)
    b.apply_load(-4, 0, -1)
    b.apply_load(-46, 6, -1)
    b.apply_load(10, 2, -1)
    b.apply_load(20, 4, -1)
    b.apply_load(3, 6, 0)
    assert b.point_cflexure() == [Rational(10, 3)]

    E = Symbol('E')
    I = Symbol('I')
    b = Beam(15, E, I)
    r0 = b.apply_support(0, type='pin')
    r10 = b.apply_support(10, type='pin')
    r15, m15 = b.apply_support(15, type='fixed')
    b.apply_rotation_hinge(12)
    b.apply_load(-10, 5, -1)
    b.apply_load(-5, 10, 0, 15)
    b.solve_for_reaction_loads(r0, r10, r15, m15)
    assert b.point_cflexure() == [Rational(1200, 163), 12, Rational(163, 12)]

    E = Symbol('E')
    I = Symbol('I')
    b = Beam(15, E, I)
    r0 = b.apply_support(0, type='pin')
    r10 = b.apply_support(10, type='pin')
    r15, m15 = b.apply_support(15, type='fixed')
    b.apply_rotation_hinge(5)
    b.apply_rotation_hinge(12)
    b.apply_load(-10, 5, -1)
    b.apply_load(-5, 10, 0, 15)
    b.solve_for_reaction_loads(r0, r10, r15, m15)
    with raises(NotImplementedError):
        b.point_cflexure()

