
def test_m_InOutArgument():
    expr = Equality(x, x**2)
    name_expr = ("mysqr", expr)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function x = mysqr(x)\n"
        "  x = x.^2;\n"
        "end\n"
    )
    assert source == expected

