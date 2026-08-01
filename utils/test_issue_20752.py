
def test_issue_20752():
    b = symbols('b', nonzero=True)
    m = Matrix([[0, 0, 0], [0, b, 0], [0, 0, b]])
    assert m.is_positive_semidefinite is None

