
def test_ccode_cse():
    a, b, c, d = symbols('a b c d')
    e = MatrixSymbol('e', 3, 1)
    name_expr = ("test", [Equality(e, Matrix([[a*b], [a*b + c*d], [a*b*c*d]]))])
    generator = CCodeGen(cse=True)
    result = codegen(name_expr, code_gen=generator, header=False, empty=False)
    source = result[0][1]
    expected = (
        '#include "test.h"\n'
        '#include <math.h>\n'
        'void test(double a, double b, double c, double d, double *e) {\n'
        '   const double x0 = a*b;\n'
        '   const double x1 = c*d;\n'
        '   e[0] = x0;\n'
        '   e[1] = x0 + x1;\n'
        '   e[2] = x0*x1;\n'
        '}\n'
    )
    assert source == expected

