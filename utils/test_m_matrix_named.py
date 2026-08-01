
def test_m_matrix_named():
    e2 = Matrix([[x, 2*y, pi*z]])
    name_expr = ("test", Equality(MatrixSymbol('myout1', 1, 3), e2))
    result = codegen(name_expr, "Octave", header=False, empty=False)
    assert result[0][0] == "test.m"
    source = result[0][1]
    expected = (
        "function myout1 = test(x, y, z)\n"
        "  myout1 = [x 2*y pi*z];\n"
        "end\n"
    )
    assert source == expected

