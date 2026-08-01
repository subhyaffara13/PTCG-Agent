
def test_convert_equals_signs():
    transformations = standard_transformations + \
                        (convert_equals_signs, )
    x = Symbol('x')
    y = Symbol('y')
    assert parse_expr("1*2=x", transformations=transformations) == Eq(2, x)
    assert parse_expr("y = x", transformations=transformations) == Eq(y, x)
    assert parse_expr("(2*y = x) = False",
        transformations=transformations) == Eq(Eq(2*y, x), False)

