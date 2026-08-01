
def test_unevaluated_mul():
    eq = Mul(x + y, x + y, evaluate=False)
    assert cse(eq) == ([(x0, x + y)], [x0**2])

