
def test_orient_axis():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    A.orient_axis(B,-B.x, 1)
    A1 = A.dcm(B)
    A.orient_axis(B, B.x, -1)
    A2 = A.dcm(B)
    A.orient_axis(B, 1, -B.x)
    A3 = A.dcm(B)
    assert A1 == A2
    assert A2 == A3
    raises(TypeError, lambda: A.orient_axis(B, 1, 1))

