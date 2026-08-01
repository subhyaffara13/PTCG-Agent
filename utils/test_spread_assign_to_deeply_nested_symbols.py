
def test_spread_assign_to_deeply_nested_symbols():
    gl = glsl_code
    a, b, c, x, y, z = symbols('a b c x y z')
    expr = (((1,2),3), ((1,2),3))
    assign_to = (((a, b), c), ((x, y), z))
    assert gl(expr, assign_to=assign_to) == textwrap.dedent('''\
        a = 1;
        b = 2;
        c = 3;
        x = 1;
        y = 2;
        z = 3;'''
    )

