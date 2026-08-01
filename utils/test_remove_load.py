
def test_remove_load():
    P1 = Point('P1')
    P2 = Point('P2')
    with warns_deprecated_sympy():
        B = Body('B')
    f1 = B.x
    f2 = B.y
    B.apply_force(f1, P1)
    B.apply_force(f2, P2)
    assert B.loads == [(P1, f1), (P2, f2)]
    B.remove_load(P2)
    assert B.loads == [(P1, f1)]
    B.apply_torque(f1.cross(f2))
    assert B.loads == [(P1, f1), (B.frame, f1.cross(f2))]
    B.remove_load()
    assert B.loads == [(P1, f1)]


def test_remove_load():
    E = Symbol('E')
    I = Symbol('I')
    b = Beam(4, E, I)

    try:
        b.remove_load(2, 1, -1)
    # As no load is applied on beam, ValueError should be returned.
    except ValueError:
        assert True
    else:
        assert False

    b.apply_load(-3, 0, -2)
    b.apply_load(4, 2, -1)
    b.apply_load(-2, 2, 2, end = 3)
    b.remove_load(-2, 2, 2, end = 3)
    assert b.load == -3*SingularityFunction(x, 0, -2) + 4*SingularityFunction(x, 2, -1)
    assert b.applied_loads == [(-3, 0, -2, None), (4, 2, -1, None)]

    try:
        b.remove_load(1, 2, -1)
    # As load of this magnitude was never applied at
    # this position, method should return a ValueError.
    except ValueError:
        assert True
    else:
        assert False

    b.remove_load(-3, 0, -2)
    b.remove_load(4, 2, -1)
    assert b.load == 0
    assert b.applied_loads == []

