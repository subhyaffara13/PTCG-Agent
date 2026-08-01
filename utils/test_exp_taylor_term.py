
def test_exp_taylor_term():
    x = symbols('x')
    assert exp(x).taylor_term(1, x) == x
    assert exp(x).taylor_term(3, x) == x**3/6
    assert exp(x).taylor_term(4, x) == x**4/24
    assert exp(x).taylor_term(-1, x) is S.Zero

