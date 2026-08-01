
def test_ansi_math2_codegen():
    # not included: frexp, ldexp, modf, fmod
    from sympy.functions.elementary.trigonometric import atan2
    x, y = symbols('x,y')
    name_expr = [
        ("test_atan2", atan2(x, y)),
        ("test_pow", x**y),
    ]
    result = codegen(name_expr, "C89", "file", header=False, empty=False)
    assert result[0][0] == "file.c"
    assert result[0][1] == (
        '#include "file.h"\n#include <math.h>\n'
        'double test_atan2(double x, double y) {\n   double test_atan2_result;\n   test_atan2_result = atan2(x, y);\n   return test_atan2_result;\n}\n'
        'double test_pow(double x, double y) {\n   double test_pow_result;\n   test_pow_result = pow(x, y);\n   return test_pow_result;\n}\n'
    )
    assert result[1][0] == "file.h"
    assert result[1][1] == (
        '#ifndef PROJECT__FILE__H\n#define PROJECT__FILE__H\n'
        'double test_atan2(double x, double y);\n'
        'double test_pow(double x, double y);\n'
        '#endif\n'
    )

