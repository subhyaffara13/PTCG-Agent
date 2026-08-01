
def test_issue_18956():
    A = Array([[1, 2], [3, 4]])
    B = Matrix([[1,2],[3,4]])
    raises(TypeError, lambda: B + A)
    raises(TypeError, lambda: A + B)


def test_issue_18956():
    A = Array([[1, 2], [3, 4]])
    B = Matrix([[1,2],[3,4]])
    raises(TypeError, lambda: B + A)
    raises(TypeError, lambda: A + B)

