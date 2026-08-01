
def test_split_symbols_numeric():
    transformations = (
        standard_transformations +
        (implicit_multiplication_application,))

    n = Symbol('n')
    expr1 = parse_expr('2**n * 3**n')
    expr2 = parse_expr('2**n3**n', transformations=transformations)
    assert expr1 == expr2 == 2**n*3**n

    expr1 = parse_expr('n12n34', transformations=transformations)
    assert expr1 == n*12*n*34

