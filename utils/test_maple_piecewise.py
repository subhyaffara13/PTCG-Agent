
def test_maple_piecewise():
    expr = Piecewise((x, x < 1), (x ** 2, True))

    assert maple_code(expr) == "piecewise(x < 1, x, x^2)"
    assert maple_code(expr, assign_to="r") == (
        "r := piecewise(x < 1, x, x^2)")

    expr = Piecewise((x ** 2, x < 1), (x ** 3, x < 2), (x ** 4, x < 3), (x ** 5, True))
    expected = "piecewise(x < 1, x^2, x < 2, x^3, x < 3, x^4, x^5)"
    assert maple_code(expr) == expected
    assert maple_code(expr, assign_to="r") == "r := " + expected

    # Check that Piecewise without a True (default) condition error
    expr = Piecewise((x, x < 1), (x ** 2, x > 1), (sin(x), x > 0))
    raises(ValueError, lambda: maple_code(expr))

