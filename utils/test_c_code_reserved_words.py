
def test_c_code_reserved_words():
    x, y, z = symbols('if, typedef, while')
    expr = (x + y) * z
    routine = make_routine("test", expr)
    code_gen = C99CodeGen()
    source = get_string(code_gen.dump_c, [routine])
    expected = (
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test(double if_, double typedef_, double while_) {\n"
        "   double test_result;\n"
        "   test_result = while_*(if_ + typedef_);\n"
        "   return test_result;\n"
        "}\n"
    )
    assert source == expected

