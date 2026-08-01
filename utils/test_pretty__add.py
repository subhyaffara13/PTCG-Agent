
def test_pretty_Add():
    eq = Mul(-2, x - 2, evaluate=False) + 5
    assert pretty(eq) == '5 - 2*(x - 2)'

