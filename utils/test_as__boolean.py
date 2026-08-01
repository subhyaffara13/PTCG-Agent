
def test_as_Boolean():
    nz = symbols('nz', nonzero=True)
    assert all(as_Boolean(i) is S.true for i in (True, S.true, 1, nz))
    z = symbols('z', zero=True)
    assert all(as_Boolean(i) is S.false for i in (False, S.false, 0, z))
    assert all(as_Boolean(i) == i for i in (x, x < 0))
    for i in (2, S(2), x + 1, []):
        raises(TypeError, lambda: as_Boolean(i))

