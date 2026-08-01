
def test_m_matrix_named_matsym():
    myout1 = MatrixSymbol('myout1', 1, 3)
    e2 = Matrix([[x, 2*y, pi*z]])
    name_expr = ("test", Equality(myout1, e2, evaluate=False))
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function myout1 = test(x, y, z)\n"
        "  myout1 = [x 2*y pi*z];\n"
        "end\n"
    )
    assert source == expected

