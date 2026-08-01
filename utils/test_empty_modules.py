
def test_empty_modules():
    x, y = symbols('x y')
    expr = -(x % y)

    no_modules = lambdify([x, y], expr)
    empty_modules = lambdify([x, y], expr, modules=[])
    assert no_modules(3, 7) == empty_modules(3, 7)
    assert no_modules(3, 7) == -3

