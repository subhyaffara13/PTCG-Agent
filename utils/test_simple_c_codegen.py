
def test_simple_c_codegen():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    expected = [
        ("file.c",
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test(double x, double y, double z) {\n"
        "   double test_result;\n"
        "   test_result = z*(x + y);\n"
        "   return test_result;\n"
        "}\n"),
        ("file.h",
        "#ifndef PROJECT__FILE__H\n"
        "#define PROJECT__FILE__H\n"
        "double test(double x, double y, double z);\n"
        "#endif\n")
    ]
    result = codegen(("test", expr), "C", "file", header=False, empty=False)
    assert result == expected

