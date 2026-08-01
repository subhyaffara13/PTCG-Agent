
def test_lame_coefficients():
    a = CoordSys3D('a', 'spherical')
    assert a.lame_coefficients() == (1, a.r, sin(a.theta)*a.r)
    a = CoordSys3D('a')
    assert a.lame_coefficients() == (1, 1, 1)
    a = CoordSys3D('a', 'cartesian')
    assert a.lame_coefficients() == (1, 1, 1)
    a = CoordSys3D('a', 'cylindrical')
    assert a.lame_coefficients() == (1, a.r, 1)

