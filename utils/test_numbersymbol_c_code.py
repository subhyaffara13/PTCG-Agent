
def test_numbersymbol_c_code():
    routine = make_routine("test", pi**Catalan)
    code_gen = C89CodeGen()
    source = get_string(code_gen.dump_c, [routine])
    expected = (
        "#include \"file.h\"\n"
        "#include <math.h>\n"
        "double test() {\n"
        "   double test_result;\n"
        "   double const Catalan = %s;\n"
        "   test_result = pow(M_PI, Catalan);\n"
        "   return test_result;\n"
        "}\n"
    ) % Catalan.evalf(17)
    assert source == expected

