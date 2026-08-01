
def test_orient_body():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient_body_fixed(A, (1,1,0), 'XYX')
    assert B.dcm(A) == Matrix([[cos(1), sin(1)**2, -sin(1)*cos(1)], [0, cos(1), sin(1)], [sin(1), -sin(1)*cos(1), cos(1)**2]])

