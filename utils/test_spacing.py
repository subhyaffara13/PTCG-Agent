
def test_spacing():
    for latex_str, sympy_expr in SPACING_RELATED_EXPRESSION_PAIRS:
        with evaluate(False):
            assert parse_latex_lark(latex_str) == sympy_expr, latex_str


def test_spacing():
    return _test_spacing(np.float64)

