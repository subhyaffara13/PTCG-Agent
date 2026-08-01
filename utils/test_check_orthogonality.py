
def test_check_orthogonality():
    x, y, z = symbols('x y z')
    u,v = symbols('u, v')
    a = CoordSys3D('a', transformation=((x, y, z), (x*sin(y)*cos(z), x*sin(y)*sin(z), x*cos(y))))
    assert a._check_orthogonality(a._transformation) is True
    a = CoordSys3D('a', transformation=((x, y, z), (x * cos(y), x * sin(y), z)))
    assert a._check_orthogonality(a._transformation) is True
    a = CoordSys3D('a', transformation=((u, v, z), (cosh(u) * cos(v), sinh(u) * sin(v), z)))
    assert a._check_orthogonality(a._transformation) is True

    raises(ValueError, lambda: CoordSys3D('a', transformation=((x, y, z), (x, x, z))))
    raises(ValueError, lambda: CoordSys3D('a', transformation=(
        (x, y, z), (x*sin(y/2)*cos(z), x*sin(y)*sin(z), x*cos(y)))))

