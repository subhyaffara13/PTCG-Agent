
def test_force_default():
    N = ReferenceFrame('N')
    Po = Point('Po')
    f1 = Force(Po, N.x)
    assert f1.point == Po
    assert f1.force == N.x
    assert f1.__repr__() == 'Force(point=Po, force=N.x)'
    # Test tuple behaviour
    assert isinstance(f1, tuple)
    assert f1[0] == Po
    assert f1[1] == N.x
    assert f1 == (Po, N.x)
    assert f1 != (N.x, Po)
    assert f1 != (Po, N.x + N.y)
    assert f1 != (Point('Co'), N.x)
    # Test body as input
    P = Particle('P', Po)
    f2 = Force(P, N.x)
    assert f1 == f2

