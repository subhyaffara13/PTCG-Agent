
def test_issue_25697():
    assert _solve_inequality(log(x, 3) <= 2, x) == (x <= 9) & (S.Zero < x)

