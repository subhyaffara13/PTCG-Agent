
def test_issue_from_PR1599():
    n1, n2, n3, n4 = symbols('n1 n2 n3 n4', negative=True)
    assert (powsimp(sqrt(n1)*sqrt(n2)*sqrt(n3)) ==
        -I*sqrt(-n1)*sqrt(-n2)*sqrt(-n3))
    assert (powsimp(root(n1, 3)*root(n2, 3)*root(n3, 3)*root(n4, 3)) ==
        -(-1)**Rational(1, 3)*
        (-n1)**Rational(1, 3)*(-n2)**Rational(1, 3)*(-n3)**Rational(1, 3)*(-n4)**Rational(1, 3))


def test_issue_from_PR1599():
    n1, n2, n3, n4 = symbols('n1 n2 n3 n4', negative=True)
    assert simplify(I*sqrt(n1)) == -sqrt(-n1)

