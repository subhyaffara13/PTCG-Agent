
def test_issue_5321():
    raises(ValueError, lambda: Matrix([[1, 2, 3], Matrix(0, 1, [])]))


def test_issue_5321():
    raises(ValueError, lambda: Matrix([[1, 2, 3], Matrix(0, 1, [])]))

