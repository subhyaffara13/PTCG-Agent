
def test_exp_expand_NC():
    A, B, C = symbols('A,B,C', commutative=False)

    assert exp(A + B).expand() == exp(A + B)
    assert exp(A + B + C).expand() == exp(A + B + C)
    assert exp(x + y).expand() == exp(x)*exp(y)
    assert exp(x + y + z).expand() == exp(x)*exp(y)*exp(z)

