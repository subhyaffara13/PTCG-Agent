
def test_matrix_of_tuples_spread_assign_to_symbols():
    gl = glsl_code
    with warns_deprecated_sympy():
        expr = Matrix([[(1,2),(3,4)],[(5,6),(7,8)]])
    assign_to = (symbols('a b'), symbols('c d'), symbols('e f'), symbols('g h'))
    assert gl(expr, assign_to) == textwrap.dedent('''\
        a = 1;
        b = 2;
        c = 3;
        d = 4;
        e = 5;
        f = 6;
        g = 7;
        h = 8;'''
    )

