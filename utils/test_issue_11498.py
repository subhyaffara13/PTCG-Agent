
def test_issue_11498():
    A = ReferenceFrame('A')
    B = ReferenceFrame('B')

    # Identity transformation
    A.orient(B, 'DCM', eye(3))
    assert A.dcm(B) == Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert B.dcm(A) == Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # x -> y
    # y -> -z
    # z -> -x
    A.orient(B, 'DCM', Matrix([[0, 1, 0], [0, 0, -1], [-1, 0, 0]]))
    assert B.dcm(A) == Matrix([[0, 1, 0], [0, 0, -1], [-1, 0, 0]])
    assert A.dcm(B) == Matrix([[0, 0, -1], [1, 0, 0], [0, -1, 0]])
    assert B.dcm(A).T == A.dcm(B)

