
def test_integral_expressions():
    expected_failures = {14}
    for i, (latex_str, sympy_expr) in enumerate(UNEVALUATED_INTEGRAL_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, i

    for i, (latex_str, sympy_expr) in enumerate(EVALUATED_INTEGRAL_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        assert parse_latex_lark(latex_str) == sympy_expr, latex_str

