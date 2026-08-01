
def test_simple_f_code():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    routine = make_routine("test", expr)
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [routine])
    expected = (
        "REAL*8 function test(x, y, z)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(in) :: z\n"
        "test = z*(x + y)\n"
        "end function\n"
    )
    assert source == expected

