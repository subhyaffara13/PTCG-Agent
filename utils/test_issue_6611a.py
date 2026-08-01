
def test_issue_6611a():
    assert Mul.flatten([3**Rational(1, 3),
        Pow(-Rational(1, 9), Rational(2, 3), evaluate=False)]) == \
        ([Rational(1, 3), (-1)**Rational(2, 3)], [], None)

