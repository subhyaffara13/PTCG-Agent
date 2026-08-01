
def test_issue_22717():
    assert solve((-y**2 + log(y**2/x) + 2, -2*x*y + 2*x/y)) == [
        {y: -1, x: E}, {y: 1, x: E}]

