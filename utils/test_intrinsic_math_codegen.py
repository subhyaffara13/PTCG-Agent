
def test_intrinsic_math_codegen():
    # not included: log10
    from sympy.functions.elementary.complexes import Abs
    from sympy.functions.elementary.exponential import log
    from sympy.functions.elementary.hyperbolic import (cosh, sinh, tanh)
    from sympy.functions.elementary.miscellaneous import sqrt
    from sympy.functions.elementary.trigonometric import (acos, asin, atan, cos, sin, tan)
    x = symbols('x')
    name_expr = [
        ("test_abs", Abs(x)),
        ("test_acos", acos(x)),
        ("test_asin", asin(x)),
        ("test_atan", atan(x)),
        ("test_cos", cos(x)),
        ("test_cosh", cosh(x)),
        ("test_log", log(x)),
        ("test_ln", log(x)),
        ("test_sin", sin(x)),
        ("test_sinh", sinh(x)),
        ("test_sqrt", sqrt(x)),
        ("test_tan", tan(x)),
        ("test_tanh", tanh(x)),
    ]
    result = codegen(name_expr, "F95", "file", header=False, empty=False)
    assert result[0][0] == "file.f90"
    expected = (
        'REAL*8 function test_abs(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_abs = abs(x)\n'
        'end function\n'
        'REAL*8 function test_acos(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_acos = acos(x)\n'
        'end function\n'
        'REAL*8 function test_asin(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_asin = asin(x)\n'
        'end function\n'
        'REAL*8 function test_atan(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_atan = atan(x)\n'
        'end function\n'
        'REAL*8 function test_cos(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_cos = cos(x)\n'
        'end function\n'
        'REAL*8 function test_cosh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_cosh = cosh(x)\n'
        'end function\n'
        'REAL*8 function test_log(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_log = log(x)\n'
        'end function\n'
        'REAL*8 function test_ln(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_ln = log(x)\n'
        'end function\n'
        'REAL*8 function test_sin(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_sin = sin(x)\n'
        'end function\n'
        'REAL*8 function test_sinh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_sinh = sinh(x)\n'
        'end function\n'
        'REAL*8 function test_sqrt(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_sqrt = sqrt(x)\n'
        'end function\n'
        'REAL*8 function test_tan(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_tan = tan(x)\n'
        'end function\n'
        'REAL*8 function test_tanh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'test_tanh = tanh(x)\n'
        'end function\n'
    )
    assert result[0][1] == expected

    assert result[1][0] == "file.h"
    expected = (
        'interface\n'
        'REAL*8 function test_abs(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_acos(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_asin(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_atan(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_cos(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_cosh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_log(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_ln(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_sin(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_sinh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_sqrt(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_tan(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
        'interface\n'
        'REAL*8 function test_tanh(x)\n'
        'implicit none\n'
        'REAL*8, intent(in) :: x\n'
        'end function\n'
        'end interface\n'
    )
    assert result[1][1] == expected

