
def test_m_simple_code_nameout():
    expr = Equality(z, (x + y))
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function z = test(x, y)\n"
        "  z = x + y;\n"
        "end\n"
    )
    assert source == expected

