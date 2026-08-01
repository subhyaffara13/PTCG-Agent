
def test_torque_default():
    N = ReferenceFrame('N')
    f1 = Torque(N, N.x)
    assert f1.frame == N
    assert f1.torque == N.x
    assert f1.__repr__() == 'Torque(frame=N, torque=N.x)'
    # Test tuple behaviour
    assert isinstance(f1, tuple)
    assert f1[0] == N
    assert f1[1] == N.x
    assert f1 == (N, N.x)
    assert f1 != (N.x, N)
    assert f1 != (N, N.x + N.y)
    assert f1 != (ReferenceFrame('A'), N.x)
    # Test body as input
    rb = RigidBody('P', frame=N)
    f2 = Torque(rb, N.x)
    assert f1 == f2

