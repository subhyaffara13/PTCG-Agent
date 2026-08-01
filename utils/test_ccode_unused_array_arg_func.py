
def test_ccode_unused_array_arg_func():
    # issue 16689
    X = MatrixSymbol('X',3,1)
    Y = MatrixSymbol('Y',3,1)
    z = symbols('z',integer = True)
    name_expr = ('testBug', X[0] + X[1])
    result = codegen(name_expr, language='C', header=False, empty=False, argument_sequence=(X, Y, z))
    source = result[0][1]
    expected = (
        '#include "testBug.h"\n'
        '#include <math.h>\n'
        'double testBug(double *X, double *Y, int z) {\n'
        '   double testBug_result;\n'
        '   testBug_result = X[0] + X[1];\n'
        '   return testBug_result;\n'
        '}\n'
    )
    assert source == expected

