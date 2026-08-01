
def test_rcode_user_functions():
    x = symbols('x', integer=False)
    n = symbols('n', integer=True)
    custom_functions = {
        "ceiling": "myceil",
        "Abs": [(lambda x: not x.is_integer, "fabs"), (lambda x: x.is_integer, "abs")],
    }
    assert rcode(ceiling(x), user_functions=custom_functions) == "myceil(x)"
    assert rcode(Abs(x), user_functions=custom_functions) == "fabs(x)"
    assert rcode(Abs(n), user_functions=custom_functions) == "abs(n)"

