
def test_custom_codegen():
    from sympy.printing.c import C99CodePrinter
    from sympy.functions.elementary.exponential import exp

    printer = C99CodePrinter(settings={'user_functions': {'exp': 'fastexp'}})

    x, y = symbols('x y')
    expr = exp(x + y)

    # replace math.h with a different header
    gen = C99CodeGen(printer=printer,
                     preprocessor_statements=['#include "fastexp.h"'])

    expected = (
        '#include "expr.h"\n'
        '#include "fastexp.h"\n'
        'double expr(double x, double y) {\n'
        '   double expr_result;\n'
        '   expr_result = fastexp(x + y);\n'
        '   return expr_result;\n'
        '}\n'
    )

    result = codegen(('expr', expr), header=False, empty=False, code_gen=gen)
    source = result[0][1]
    assert source == expected

    # use both math.h and an external header
    gen = C99CodeGen(printer=printer)
    gen.preprocessor_statements.append('#include "fastexp.h"')

    expected = (
        '#include "expr.h"\n'
        '#include <math.h>\n'
        '#include "fastexp.h"\n'
        'double expr(double x, double y) {\n'
        '   double expr_result;\n'
        '   expr_result = fastexp(x + y);\n'
        '   return expr_result;\n'
        '}\n'
    )

    result = codegen(('expr', expr), header=False, empty=False, code_gen=gen)
    source = result[0][1]
    assert source == expected

