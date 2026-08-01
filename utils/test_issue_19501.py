
def test_issue_19501():
    x = Symbol('x')
    eq = parse_expr('E**x(1+x)', local_dict={'x': x}, transformations=(
        standard_transformations +
        (implicit_multiplication_application,)))
    assert eq.free_symbols == {x}

