
def test_user_functions():
    x = symbols('x')
    assert fcode(sin(x), user_functions={"sin": "zsin"}) == "      zsin(x)"
    x = symbols('x')
    assert fcode(
        gamma(x), user_functions={"gamma": "mygamma"}) == "      mygamma(x)"
    g = Function('g')
    assert fcode(g(x), user_functions={"g": "great"}) == "      great(x)"
    n = symbols('n', integer=True)
    assert fcode(
        factorial(n), user_functions={"factorial": "fct"}) == "      fct(n)"


def test_user_functions():
    x = symbols('x', integer=False)
    n = symbols('n', integer=True)
    custom_functions = {
        "ceiling": "ceil",
        "Abs": [(lambda x: not x.is_integer, "fabs", 4), (lambda x: x.is_integer, "abs", 4)],
    }
    assert rust_code(ceiling(x), user_functions=custom_functions) == "x.ceil()"
    assert rust_code(Abs(x), user_functions=custom_functions) == "fabs(x)"
    assert rust_code(Abs(n), user_functions=custom_functions) == "abs(n)"

