
def test_ccode_sign():
    expr1, ref1 = sign(x) * y, 'y*(((x) > 0) - ((x) < 0))'
    expr2, ref2 = sign(cos(x)), '(((cos(x)) > 0) - ((cos(x)) < 0))'
    expr3, ref3 = sign(2 * x + x**2) * x + x**2, 'pow(x, 2) + x*(((pow(x, 2) + 2*x) > 0) - ((pow(x, 2) + 2*x) < 0))'
    assert ccode(expr1) == ref1
    assert ccode(expr1, 'z') == 'z = %s;' % ref1
    assert ccode(expr2) == ref2
    assert ccode(expr3) == ref3

