
def test_m_multifcns_per_file():
    name_expr = [ ("foo", [2*x, 3*y]), ("bar", [y**2, 4*y]) ]
    result = codegen(name_expr, "Octave", header=False, empty=False)
    assert result[0][0] == "foo.m"
    source = result[0][1]
    expected = (
        "function [out1, out2] = foo(x, y)\n"
        "  out1 = 2*x;\n"
        "  out2 = 3*y;\n"
        "end\n"
        "function [out1, out2] = bar(y)\n"
        "  out1 = y.^2;\n"
        "  out2 = 4*y;\n"
        "end\n"
    )
    assert source == expected

