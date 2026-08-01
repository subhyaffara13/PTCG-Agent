
def test_numbersymbol_f_code():
    routine = make_routine("test", pi**Catalan)
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [routine])
    expected = (
        "REAL*8 function test()\n"
        "implicit none\n"
        "REAL*8, parameter :: Catalan = %sd0\n"
        "REAL*8, parameter :: pi = %sd0\n"
        "test = pi**Catalan\n"
        "end function\n"
    ) % (Catalan.evalf(17), pi.evalf(17))
    assert source == expected

