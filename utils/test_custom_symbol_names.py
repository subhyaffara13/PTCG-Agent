
def test_custom_symbol_names():
    x = Symbol('x')
    y = Symbol('y')
    assert latex(x) == r"x"
    assert latex(x, symbol_names={x: "x_i"}) == r"x_i"
    assert latex(x + y, symbol_names={x: "x_i"}) == r"x_i + y"
    assert latex(x**2, symbol_names={x: "x_i"}) == r"x_i^{2}"
    assert latex(x + y, symbol_names={x: "x_i", y: "y_j"}) == r"x_i + y_j"

