
def test_rcode_sinc():
    from sympy.functions.elementary.trigonometric import sinc
    expr = sinc(x)
    res = rcode(expr)
    ref = "(ifelse(x != 0,sin(x)/x,1))"
    assert res == ref

