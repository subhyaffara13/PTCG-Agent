
def test_relation_expressions():
    for latex_str, sympy_expr in RELATION_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

