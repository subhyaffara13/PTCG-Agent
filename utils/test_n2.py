
def test_N2():
    x = symbols('x', real=True)
    assert ask(x**4 - x + 1 > 0) is True
    assert ask(x**4 - x + 1 > 1) is False

