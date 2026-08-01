
def test_applied_function_expressions():
    expected_failures = {0, 3, 4}  # 0 is ambiguous, and the others require not-yet-added features
    # not sure why 1, and 2 are failing
    for i, (latex_str, sympy_expr) in enumerate(APPLIED_FUNCTION_EXPRESSION_PAIRS):
        if i in expected_failures:
            continue
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str

