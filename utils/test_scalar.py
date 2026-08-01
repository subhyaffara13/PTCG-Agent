
def test_scalar():
    from sympy.vector import CoordSys3D
    C = CoordSys3D('C')
    v1 = 3*C.i + 4*C.j + 5*C.k
    v2 = 3*C.i - 4*C.j + 5*C.k
    assert v1.is_Vector is True
    assert v1.is_scalar is False
    assert (v1.dot(v2)).is_scalar is True
    assert (v1.cross(v2)).is_scalar is False


def test_scalar(val, signed, transform):
    val = -val if signed else val
    assert to_numeric(transform(val)) == float(val)

