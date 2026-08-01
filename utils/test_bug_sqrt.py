
def test_bug_sqrt():
    assert ((sqrt(Rational(2)) + 1)*(sqrt(Rational(2)) - 1)).expand() == 1

