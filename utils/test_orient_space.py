
def test_orient_space():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    B.orient_space_fixed(A, (0,0,0), '123')
    assert B.dcm(A) == Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

