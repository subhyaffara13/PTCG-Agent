
def test_square_root_expressions():
    for latex_str, sympy_expr in UNEVALUATED_SQRT_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

    for latex_str, sympy_expr in EVALUATED_SQRT_EXPRESSION_PAIRS:
        assert parse_latex_lark(latex_str) == sympy_expr, latex_str

