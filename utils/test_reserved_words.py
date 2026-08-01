
def test_reserved_words():

    x, y = symbols("x if")

    expr = sin(y)
    assert rust_code(expr) == "if_.sin()"
    assert rust_code(expr, dereference=[y]) == "(*if_).sin()"
    assert rust_code(expr, reserved_word_suffix='_unreserved') == "if_unreserved.sin()"

    with raises(ValueError):
        rust_code(expr, error_on_reserved=True)

