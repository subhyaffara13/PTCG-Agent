
def test_issue_23432():
    expr = 1/sqrt(1 - x**2)
    result = expr.series(x, 0.5)
    assert result.is_Add and len(result.args) == 7

