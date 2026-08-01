
def test_orient_quaternion():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient_quaternion(A, (0,0,0,0))
    assert B.dcm(A) == Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

