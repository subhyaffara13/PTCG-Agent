
def test_product_expressions():
    for latex_str, sympy_expr in UNEVALUATED_PRODUCT_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

