
def test_m_results_matrix_named_ordered():
    B, C = symbols('B,C')
    A = MatrixSymbol('A', 1, 3)
    expr1 = Equality(C, (x + y)*z)
    expr2 = Equality(A, Matrix([[1, 2, x]]))
    expr3 = Equality(B, 2*x)
    name_expr = ("test", [expr1, expr2, expr3])
    result, = codegen(name_expr, "Octave", header=False, empty=False,
                     argument_sequence=(x, z, y))
    source = result[1]
    expected = (
        "function [C, A, B] = test(x, z, y)\n"
        "  C = z.*(x + y);\n"
        "  A = [1 2 x];\n"
        "  B = 2*x;\n"
        "end\n"
    )
    assert source == expected

