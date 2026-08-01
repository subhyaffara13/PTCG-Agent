
def test_ccode_sinc():
    from sympy.functions.elementary.trigonometric import sinc
    expr = sinc(x)
    assert ccode(expr) == (
            "(((x != 0) ? (\n"
            "   sin(x)/x\n"
            ")\n"
            ": (\n"
            "   1\n"
            ")))")

