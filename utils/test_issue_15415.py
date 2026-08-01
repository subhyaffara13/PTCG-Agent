
def test_issue_15415():
    assert solve(x - 3, x) == [3]
    assert solve([x - 3], x) == {x:3}
    assert solve(Eq(y + 3*x**2/2, y + 3*x), y) == []
    assert solve([Eq(y + 3*x**2/2, y + 3*x)], y) == []
    assert solve([Eq(y + 3*x**2/2, y + 3*x), Eq(x, 1)], y) == []

