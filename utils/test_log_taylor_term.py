
def test_log_taylor_term():
    x = symbols('x')
    assert log(x).taylor_term(0, x) == x
    assert log(x).taylor_term(1, x) == -x**2/2
    assert log(x).taylor_term(4, x) == x**5/5
    assert log(x).taylor_term(-1, x) is S.Zero

