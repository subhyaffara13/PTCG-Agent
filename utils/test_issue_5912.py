
def test_issue_5912():
    assert set(solve(x**2 - x - 0.1, rational=True)) == \
        {S.Half + sqrt(35)/10, -sqrt(35)/10 + S.Half}
    ans = solve(x**2 - x - 0.1, rational=False)
    assert len(ans) == 2 and all(a.is_Number for a in ans)
    ans = solve(x**2 - x - 0.1)
    assert len(ans) == 2 and all(a.is_Number for a in ans)

