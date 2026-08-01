
def test_has_units():
    from sympy.physics.units import m, s

    assert (x*m/s).has(x)
    assert (x*m/s).has(y, z) is False

