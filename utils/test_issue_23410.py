
def test_issue_23410():
    A = Matrix([[1, 12], [0, 8], [0, 5]])
    H = Matrix([[1, 0], [0, 8], [0, 5]])
    assert hermite_normal_form(A) == H

