
def test_c_code_argument_order():
    x, y, z = symbols('x,y,z')
    expr = x + y
    routine = make_routine("test", expr, argument_sequence=[z, x, y])
    code_gen = C89CodeGen()
    source = get_string(code_gen.dump_c, [routine])
    expected = (
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test(double z, double x, double y) {\n"
        "   double test_result;\n"
        "   test_result = x + y;\n"
        "   return test_result;\n"
        "}\n"
    )
    assert source == expected

