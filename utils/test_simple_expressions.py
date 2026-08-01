
def test_simple_expressions():
    expected_failures = {20}
    for i, (latex_str, sympy_expr) in enumerate(UNEVALUATED_SIMPLE_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

    for i, (latex_str, sympy_expr) in enumerate(EVALUATED_SIMPLE_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        assert parse_latex_lark(latex_str) == sympy_expr, latex_str

