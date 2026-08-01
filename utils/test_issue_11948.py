
def test_issue_11948():
    A = MatrixSymbol('A', 3, 3)
    a = Wild('a')
    assert A.match(a) == {a: A}


def test_issue_11948():
    A = MatrixSymbol('A', 3, 3)
    a = Wild('a')
    assert A.match(a) == {a: A}

