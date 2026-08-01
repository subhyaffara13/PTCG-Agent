
def test_overloaded_operators():
    a, b, c, d, e, f = symbols('a, b, c, d, e, f')
    N = ReferenceFrame('N')
    v1 = a*N.x + b*N.y + c*N.z
    v2 = d*N.x + e*N.y + f*N.z

    assert v1 + v2 == v2 + v1
    assert v1 - v2 == -v2 + v1
    assert v1 & v2 == v2 & v1
    assert v1 ^ v2 == v1.cross(v2)
    assert v2 ^ v1 == v2.cross(v1)

