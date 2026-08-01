
def test_dereference_printing():
    expr = x + y + sin(z) + z
    assert ccode(expr, dereference=[z]) == "x + y + (*z) + sin((*z))"


def test_dereference_printing():
    expr = x + y + sin(z) + z
    assert rcode(expr, dereference=[z]) == "x + y + (*z) + sin((*z))"


def test_dereference_printing():
    expr = x + y + sin(z) + z
    assert rust_code(expr, dereference=[z]) == "x + y + (*z) + (*z).sin()"

