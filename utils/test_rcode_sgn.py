
def test_rcode_sgn():

    expr = sign(x) * y
    assert rcode(expr) == 'y*sign(x)'
    p = rcode(expr, 'z')
    assert p  == 'z = y*sign(x);'

    p = rcode(sign(2 * x + x**2) * x + x**2)
    assert p  == "x^2 + x*sign(x^2 + 2*x)"

    expr = sign(cos(x))
    p = rcode(expr)
    assert p == 'sign(cos(x))'

