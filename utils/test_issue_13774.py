
def test_issue_13774():
    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    v = [1, 1, 1]
    raises(TypeError, lambda: M*v)
    raises(TypeError, lambda: v*M)


def test_issue_13774():
    M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    v = [1, 1, 1]
    raises(TypeError, lambda: M*v)
    raises(TypeError, lambda: v*M)

