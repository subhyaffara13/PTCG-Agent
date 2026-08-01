
def test_issue_15872():
    A = Matrix([[1, 1, 1, 0], [-2, -1, 0, -1], [0, 0, -1, -1], [0, 0, 2, 1]])
    B = A - Matrix.eye(4) * I
    assert B.rank() == 3
    assert (B**2).rank() == 2
    assert (B**3).rank() == 2


def test_issue_15872():
    A = Matrix([[1, 1, 1, 0], [-2, -1, 0, -1], [0, 0, -1, -1], [0, 0, 2, 1]])
    B = A - Matrix.eye(4) * I
    assert B.rank() == 3
    assert (B**2).rank() == 2
    assert (B**3).rank() == 2

