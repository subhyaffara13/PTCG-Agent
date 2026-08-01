
def test_vector_angle():
    A = ReferenceFrame('A')
    v1 = A.x + A.y
    v2 = A.z
    assert v1.angle_between(v2) == pi/2
    B = ReferenceFrame('B')
    B.orient_axis(A, A.x, pi)
    v3 = A.x
    v4 = B.x
    assert v3.angle_between(v4) == 0

