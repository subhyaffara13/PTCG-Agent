
def test_parse_loads():
    N = ReferenceFrame('N')
    po = Point('po')
    assert _parse_load(Force(po, N.z)) == (po, N.z)
    assert _parse_load(Torque(N, N.x)) == (N, N.x)
    f1 = _parse_load((po, N.x))  # Test whether a force is recognized
    assert isinstance(f1, Force)
    assert f1 == Force(po, N.x)
    t1 = _parse_load((N, N.y))  # Test whether a torque is recognized
    assert isinstance(t1, Torque)
    assert t1 == Torque(N, N.y)
    # Bodies should be undetermined (even in case of a Particle)
    raises(ValueError, lambda: _parse_load((Particle('pa', po), N.x)))
    raises(ValueError, lambda: _parse_load((RigidBody('pa', po, N), N.x)))
    # Invalid tuple length
    raises(ValueError, lambda: _parse_load((po, N.x, po, N.x)))
    # Invalid type
    raises(TypeError, lambda: _parse_load([po, N.x]))

