
def test_issue_20902():
    f = (t / ((1 + t) ** 2))
    assert solve(f.subs({t: 3 * x + 2}).diff(x) > 0, x) == (S(-1) < x) & (x < S(-1)/3)
    assert solve(f.subs({t: 3 * x + 3}).diff(x) > 0, x) == (S(-4)/3 < x) & (x < S(-2)/3)
    assert solve(f.subs({t: 3 * x + 4}).diff(x) > 0, x) == (S(-5)/3 < x) & (x < S(-1))
    assert solve(f.subs({t: 3 * x + 2}).diff(x) > 0, x) == (S(-1) < x) & (x < S(-1)/3)

