
def test_issue_23276():
    M = Matrix([x, y])
    assert integrate(M, (x, 0, 1), (y, 0, 1)) == Matrix([
        [S.Half],
        [S.Half]])


def test_issue_23276():
    M = Matrix([x, y])
    assert integrate(M, (x, 0, 1), (y, 0, 1)) == Matrix([
        [S.Half],
        [S.Half]])

