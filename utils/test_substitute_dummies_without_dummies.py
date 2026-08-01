
def test_substitute_dummies_without_dummies():
    i, j = symbols('i,j')
    assert substitute_dummies(att(i, j) + 2) == att(i, j) + 2
    assert substitute_dummies(att(i, j) + 1) == att(i, j) + 1

