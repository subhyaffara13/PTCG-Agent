import os

def runtest_issue_10274(language, backend):
    expr = (a - b + c)**(13)
    tmp = tempfile.mkdtemp()
    f = autowrap(expr, language, backend, tempdir=tmp,
                 helpers=('helper', a - b + c, (a, b, c)))
    assert f(1, 1, 1) == 1

    for file in os.listdir(tmp):
        if not (file.startswith("wrapped_code_") and file.endswith(".c")):
            continue

        with open(tmp + '/' + file) as fil:
            lines = fil.readlines()
            assert lines[0] == "/******************************************************************************\n"
            assert "Code generated with SymPy " + sympy.__version__ in lines[1]
            assert lines[2:] == [
                " *                                                                            *\n",
                " *              See http://www.sympy.org/ for more information.               *\n",
                " *                                                                            *\n",
                " *                      This file is part of 'autowrap'                       *\n",
                " ******************************************************************************/\n",
                "#include " + '"' + file[:-1]+ 'h"' + "\n",
                "#include <math.h>\n",
                "\n",
                "double helper(double a, double b, double c) {\n",
                "\n",
                "   double helper_result;\n",
                "   helper_result = a - b + c;\n",
                "   return helper_result;\n",
                "\n",
                "}\n",
                "\n",
                "double autofunc(double a, double b, double c) {\n",
                "\n",
                "   double autofunc_result;\n",
                "   autofunc_result = pow(helper(a, b, c), 13);\n",
                "   return autofunc_result;\n",
                "\n",
                "}\n",
                ]

