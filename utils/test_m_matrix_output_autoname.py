
def test_m_matrix_output_autoname():
    expr = Matrix([[x, x+y, 3]])
    name_expr = ("test", expr)
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function out1 = test(x, y)\n"
        "  out1 = [x x + y 3];\n"
        "end\n"
    )
    assert source == expected

