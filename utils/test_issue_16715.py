
def test_issue_16715():
    raises(NotImplementedError, lambda: Piecewise((x, x<0), (0, y>1)).as_expr_set_pairs())

