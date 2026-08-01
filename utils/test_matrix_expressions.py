
def test_matrix_expressions():
    n = symbols('n', integer=True)
    A = MatrixSymbol("A", n, n)
    B = MatrixSymbol("B", n, n)
    sT(A, "MatrixSymbol(Str('A'), Symbol('n', integer=True), Symbol('n', integer=True))")
    sT(A*B, "MatMul(MatrixSymbol(Str('A'), Symbol('n', integer=True), Symbol('n', integer=True)), MatrixSymbol(Str('B'), Symbol('n', integer=True), Symbol('n', integer=True)))")
    sT(A + B, "MatAdd(MatrixSymbol(Str('A'), Symbol('n', integer=True), Symbol('n', integer=True)), MatrixSymbol(Str('B'), Symbol('n', integer=True), Symbol('n', integer=True)))")


def test_matrix_expressions():
    for latex_str, sympy_expr in UNEVALUATED_MATRIX_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

    for latex_str, sympy_expr in EVALUATED_MATRIX_EXPRESSION_PAIRS:
        assert parse_latex_lark(latex_str) == sympy_expr, latex_str

