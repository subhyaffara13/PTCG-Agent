
def test_literal_complex_number_expressions():
    for latex_str, sympy_expr in UNEVALUATED_LITERAL_COMPLEX_NUMBER_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

