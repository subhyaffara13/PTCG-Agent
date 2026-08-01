
def test_m_simple_code():
    name_expr = ("test", (x + y)*z)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    assert result[0] == "test.m"
    source = result[1]
    expected = (
        "function out1 = test(x, y, z)\n"
        "  out1 = z.*(x + y);\n"
        "end\n"
    )
    assert source == expected

