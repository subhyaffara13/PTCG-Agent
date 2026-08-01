
def test_power_expressions():
    expected_failures = {3}
    for i, (latex_str, sympy_expr) in enumerate(UNEVALUATED_POWER_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

    for i, (latex_str, sympy_expr) in enumerate(EVALUATED_POWER_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        assert parse_latex_lark(latex_str) == sympy_expr, latex_str

