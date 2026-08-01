
def test_issue_10933():
    assert solve(x**4 + y*(x + 0.1), x)  # doesn't fail
    assert solve(I*x**4 + x**3 + x**2 + 1.)  # doesn't fail

