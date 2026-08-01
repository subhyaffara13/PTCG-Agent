
def test_erf_f_code():
    x = symbols('x')
    routine = make_routine("test", erf(x) - erf(-2 * x))
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [routine])
    expected = (
        "REAL*8 function test(x)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "test = erf(x) + erf(2.0d0*x)\n"
        "end function\n"
    )
    assert source == expected, source

