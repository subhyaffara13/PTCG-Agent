
def test_symbol_expressions():
    expected_failures = {6, 7}
    for i, (latex_str, sympy_expr) in enumerate(SYMBOL_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

