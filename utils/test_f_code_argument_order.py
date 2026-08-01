
def test_f_code_argument_order():
    x, y, z = symbols('x,y,z')
    expr = x + y
    routine = make_routine("test", expr, argument_sequence=[z, x, y])
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [routine])
    expected = (
        "REAL*8 function test(z, x, y)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: z\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "test = x + y\n"
        "end function\n"
    )
    assert source == expected

