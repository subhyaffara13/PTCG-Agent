
def test_m_matrixsymbol_slice3():
    A = MatrixSymbol('A', 8, 7)
    B = MatrixSymbol('B', 2, 2)
    C = MatrixSymbol('C', 4, 2)
    name_expr = ("test", [Equality(B, A[6:, 1::3]),
                          Equality(C, A[::2, ::3])])
    result, = codegen(name_expr, "Octave", header=False, empty=False)
    source = result[1]
    expected = (
        "function [B, C] = test(A)\n"
        "  B = A(7:end, 2:3:end);\n"
        "  C = A(1:2:end, 1:3:end);\n"
        "end\n"
    )
    assert source == expected

