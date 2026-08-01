
def test_issue_8353():
    assert minimal_polynomial(exp(3*I*pi, evaluate=False), x) == x + 1
    assert minimal_polynomial(Pow(8, S(1)/3, evaluate=False), x
        ) == x - 2

