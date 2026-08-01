
def test_checking():
    assert set(
        solve(x*(x - y/x), x, check=False)) == {sqrt(y), S.Zero, -sqrt(y)}
    assert set(solve(x*(x - y/x), x, check=True)) == {sqrt(y), -sqrt(y)}
    # {x: 0, y: 4} sets denominator to 0 in the following so system should return None
    assert solve((1/(1/x + 2), 1/(y - 3) - 1)) == []
    # 0 sets denominator of 1/x to zero so None is returned
    assert solve(1/(1/x + 2)) == []

