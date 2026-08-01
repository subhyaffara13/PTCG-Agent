
def test_fcode_complex():
    import sympy.utilities.codegen
    sympy.utilities.codegen.COMPLEX_ALLOWED = True
    x = Symbol('x', real=True)
    y = Symbol('y',real=True)
    result = codegen(('test',x+y), 'f95', 'test', header=False, empty=False)
    source = (result[0][1])
    expected = (
        "REAL*8 function test(x, y)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "test = x + y\n"
        "end function\n")
    assert source == expected
    x = Symbol('x')
    y = Symbol('y',real=True)
    result = codegen(('test',x+y), 'f95', 'test', header=False, empty=False)
    source = (result[0][1])
    expected = (
        "COMPLEX*16 function test(x, y)\n"
        "implicit none\n"
        "COMPLEX*16, intent(in) :: x\n"
        "REAL*8, intent(in) :: y\n"
        "test = x + y\n"
        "end function\n"
        )
    assert source==expected
    sympy.utilities.codegen.COMPLEX_ALLOWED = False


def test_fcode_complex():
    assert fcode(I) == "      cmplx(0,1)"
    x = symbols('x')
    assert fcode(4*I) == "      cmplx(0,4)"
    assert fcode(3 + 4*I) == "      cmplx(3,4)"
    assert fcode(3 + 4*I + x) == "      cmplx(3,4) + x"
    assert fcode(I*x) == "      cmplx(0,1)*x"
    assert fcode(3 + 4*I - x) == "      cmplx(3,4) - x"
    x = symbols('x', imaginary=True)
    assert fcode(5*x) == "      5*x"
    assert fcode(I*x) == "      cmplx(0,1)*x"
    assert fcode(3 + x) == "      x + 3"

