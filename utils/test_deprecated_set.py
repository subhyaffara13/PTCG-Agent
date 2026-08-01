
def test_deprecated_set():
    with warns_deprecated_sympy():
        lambdify({x, y}, x + y)

