
def test_Matrices_1x7_spread_assign_to_symbols():
    gl = glsl_code
    A = Matrix([1,2,3,4,5,6,7])
    assign_to = symbols('x.a x.b x.c x.d x.e x.f x.g')
    assert gl(A, assign_to=assign_to) == textwrap.dedent('''\
        x.a = 1;
        x.b = 2;
        x.c = 3;
        x.d = 4;
        x.e = 5;
        x.f = 6;
        x.g = 7;'''
    )

