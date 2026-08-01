
def test_split_symbols():
    transformations = standard_transformations + \
                      (split_symbols, implicit_multiplication,)
    x = Symbol('x')
    y = Symbol('y')
    xy = Symbol('xy')


    assert parse_expr("xy") == xy
    assert parse_expr("xy", transformations=transformations) == x*y

