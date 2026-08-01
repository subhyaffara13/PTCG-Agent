
def test_functional_exponent():
    t = standard_transformations + (convert_xor, function_exponentiation)
    x = Symbol('x')
    y = Symbol('y')
    a = Symbol('a')
    yfcn = Function('y')
    assert parse_expr("sin^2(x)", transformations=t) == (sin(x))**2
    assert parse_expr("sin^y(x)", transformations=t) == (sin(x))**y
    assert parse_expr("exp^y(x)", transformations=t) == (exp(x))**y
    assert parse_expr("E^y(x)", transformations=t) == exp(yfcn(x))
    assert parse_expr("a^y(x)", transformations=t) == a**(yfcn(x))

