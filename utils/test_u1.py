
def test_U1():
    x = symbols('x', real=True)
    assert diff(abs(x), x) == sign(x)

