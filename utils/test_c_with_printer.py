
def test_c_with_printer():
    # issue 13586
    from sympy.printing.c import C99CodePrinter
    class CustomPrinter(C99CodePrinter):
        def _print_Pow(self, expr):
            return "fastpow({}, {})".format(self._print(expr.base),
                                            self._print(expr.exp))

    x = symbols('x')
    expr = x**3
    expected =[
        ("file.c",
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test(double x) {\n"
        "   double test_result;\n"
        "   test_result = fastpow(x, 3);\n"
        "   return test_result;\n"
        "}\n"),
        ("file.h",
        "#ifndef PROJECT__FILE__H\n"
        "#define PROJECT__FILE__H\n"
        "double test(double x);\n"
        "#endif\n")
    ]
    result = codegen(("test", expr), "C","file", header=False, empty=False, printer = CustomPrinter())
    assert result == expected

