
def test_cross_xfail():
    v1 = C.x * i + C.z * C.z * j
    v2 = C.x * i + C.y * j + C.z * k
    assert Cross(v1, v2) + Cross(v2, v1) == Vector.zero

