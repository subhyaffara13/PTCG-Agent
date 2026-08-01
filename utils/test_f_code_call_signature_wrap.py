
def test_f_code_call_signature_wrap():
    # Issue #7934
    x = symbols('x:20')
    expr = 0
    for sym in x:
        expr += sym
    routine = make_routine("test", expr)
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [routine])
    expected = """\
REAL*8 function test(x0, x1, x10, x11, x12, x13, x14, x15, x16, x17, x18, &
      x19, x2, x3, x4, x5, x6, x7, x8, x9)
implicit none
REAL*8, intent(in) :: x0
REAL*8, intent(in) :: x1
REAL*8, intent(in) :: x10
REAL*8, intent(in) :: x11
REAL*8, intent(in) :: x12
REAL*8, intent(in) :: x13
REAL*8, intent(in) :: x14
REAL*8, intent(in) :: x15
REAL*8, intent(in) :: x16
REAL*8, intent(in) :: x17
REAL*8, intent(in) :: x18
REAL*8, intent(in) :: x19
REAL*8, intent(in) :: x2
REAL*8, intent(in) :: x3
REAL*8, intent(in) :: x4
REAL*8, intent(in) :: x5
REAL*8, intent(in) :: x6
REAL*8, intent(in) :: x7
REAL*8, intent(in) :: x8
REAL*8, intent(in) :: x9
test = x0 + x1 + x10 + x11 + x12 + x13 + x14 + x15 + x16 + x17 + x18 + &
      x19 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9
end function
"""
    assert source == expected

