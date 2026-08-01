
def test_simple_c_code():
    x, y, z = symbols('x,y,z')
    expr = (x + y)*z
    routine = make_routine("test", expr)
    code_gen = C89CodeGen()
    source = get_string(code_gen.dump_c, [routine])
    expected = (
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test(double x, double y, double z) {\n"
        "   double test_result;\n"
        "   test_result = z*(x + y);\n"
        "   return test_result;\n"
        "}\n"
    )
    assert source == expected

