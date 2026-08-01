
def test_spread_assign_to_nested_symbols():
    gl = glsl_code
    expr = ((1,2,3), (1,2,3))
    assign_to = (symbols('a b c'), symbols('x y z'))
    assert gl(expr, assign_to=assign_to) == textwrap.dedent('''\
        a = 1;
        b = 2;
        c = 3;
        x = 1;
        y = 2;
        z = 3;'''
    )

