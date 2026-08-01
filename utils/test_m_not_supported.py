
def test_m_not_supported():
    f = Function('f')
    name_expr = ("test", [f(x).diff(x), S.ComplexInfinity])
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function [out1, out2] = test(x)\n"
        "  % unsupported: Derivative(f(x), x)\n"
        "  % unsupported: zoo\n"
        "  out1 = Derivative(f(x), x);\n"
        "  out2 = zoo;\n"
        "end\n"
    )
    assert source == expected

