
def test_global_vars():
    x, y, z, t = symbols("x y z t")
    result = codegen(('f', x*y), "F95", header=False, empty=False,
                     global_vars=(y,))
    source = result[0][1]
    expected = (
        "REAL*8 function f(x)\n"
        "implicit none\n"
        "REAL*8, intent(in) :: x\n"
        "f = x*y\n"
        "end function\n"
        )
    assert source == expected

    expected = (
        '#include "f.h"\n'
        '#include <math.h>\n'
        'double f(double x, double y) {\n'
        '   double f_result;\n'
        '   f_result = x*y + z;\n'
        '   return f_result;\n'
        '}\n'
    )
    result = codegen(('f', x*y+z), "C", header=False, empty=False,
                     global_vars=(z, t))
    source = result[0][1]
    assert source == expected

