
def test_intrinsic_math2_codegen():
    # not included: frexp, ldexp, modf, fmod
    from sympy.functions.elementary.trigonometric import atan2
    x, y = symbols('x,y')
    name_expr = [
        ("test_atan2", atan2(x, y)),
        ("test_pow", x**y),
    ]
    result = codegen(name_expr, "F95", "file", header=False, empty=False)
    assert result[0][0] == "file.f90"
    expected = (
        'REAL*8 function test_atan2(x, y)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'REAL*8, intent(in) :: y\n'
        'test_atan2 = atan2(x, y)\n'
        'end function\n'
        'REAL*8 function test_pow(x, y)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'REAL*8, intent(in) :: y\n'
        'test_pow = x**y\n'
        'end function\n'
    )
    assert result[0][1] == expected

    assert result[1][0] == "file.h"
    expected = (
        'interface\n'
        'REAL*8 function test_atan2(x, y)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'REAL*8, intent(in) :: y\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_pow(x, y)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'REAL*8, intent(in) :: y\n'
        'end function\n'
        'end interface\n'
    )
    assert result[1][1] == expected

