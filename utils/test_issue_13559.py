
def test_issue_13559():
    from sympy.parsing.sympy_parser import parse_expr
    expr = parse_expr('5/1', evaluate=False)
    assert latex(expr) == r"\frac{5}{1}"

