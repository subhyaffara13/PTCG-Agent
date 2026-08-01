
def test_rcode_Pow():
    assert rcode(x**3) == "x^3"
    assert rcode(x**(y**3)) == "x^(y^3)"
    g = implemented_function('g', Lambda(x, 2*x))
    assert rcode(1/(g(x)*3.5)**(x - y**x)/(x**2 + y)) == \
        "(3.5*2*x)^(-x + y^x)/(x^2 + y)"
    assert rcode(x**-1.0) == '1.0/x'
    assert rcode(x**Rational(2, 3)) == 'x^(2.0/3.0)'
    _cond_cfunc = [(lambda base, exp: exp.is_integer, "dpowi"),
                   (lambda base, exp: not exp.is_integer, "pow")]
    assert rcode(x**3, user_functions={'Pow': _cond_cfunc}) == 'dpowi(x, 3)'
    assert rcode(x**3.2, user_functions={'Pow': _cond_cfunc}) == 'pow(x, 3.2)'

