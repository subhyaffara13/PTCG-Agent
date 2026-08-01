
def test_simple_f_header():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    routine = make_routine("test", expr)
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_h, [routine])
    expected = (
        "interface\n"
        "REAL*8 function test(x, y, z)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "REAL*8, intent(in) :: z\n"
        "end function\n"
        "end interface\n"
    )
    assert source == expected

