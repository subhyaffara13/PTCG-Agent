
def test_MatrixSymbol_bold():
    # Issue #15871
    from sympy.matrices.expressions.trace import trace
    A = MatrixSymbol("A", 2, 2)
    assert latex(trace(A), mat_symbol_style='bold') == \
        r"\operatorname{tr}\left(\mathbf{A} \right)"
    assert latex(trace(A), mat_symbol_style='plain') == \
        r"\operatorname{tr}\left(A \right)"

    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    C = MatrixSymbol("C", 3, 3)

    assert latex(-A, mat_symbol_style='bold') == r"- \mathbf{A}"
    assert latex(A - A*B - B, mat_symbol_style='bold') == \
        r"\mathbf{A} - \mathbf{A} \mathbf{B} - \mathbf{B}"
    assert latex(-A*B - A*B*C - B, mat_symbol_style='bold') == \
        r"- \mathbf{A} \mathbf{B} - \mathbf{A} \mathbf{B} \mathbf{C} - \mathbf{B}"

    A_k = MatrixSymbol("A_k", 3, 3)
    assert latex(A_k, mat_symbol_style='bold') == r"\mathbf{A}_{k}"

    A = MatrixSymbol(r"\nabla_k", 3, 3)
    assert latex(A, mat_symbol_style='bold') == r"\mathbf{\nabla}_{k}"

