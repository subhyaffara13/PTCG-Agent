
def test_W2():
    # The function has a pole at y.
    # The integral is divergent but SymPy returns -2
    # https://github.com/sympy/sympy/issues/7160
    # Test case in Macsyma:
    # (c6) errcatch(integrate(1/(x - a)^2, x, a - 1, a + 1));
    # Integral is divergent
    assert integrate(1/(x - y)**2, (x, y - 1, y + 1)) is zoo

