
def test_W1():
    # The function has a pole at y.
    # The integral has a Cauchy principal value of zero but SymPy returns -I*pi
    # https://github.com/sympy/sympy/issues/7159
    assert integrate(1/(x - y), (x, y - 1, y + 1)) == 0

