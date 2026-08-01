
def test_issue_11553():
    eq1 = x + y + 1
    eq2 = x + GoldenRatio
    assert solve([eq1, eq2], x, y) == {x: -GoldenRatio, y: -1 + GoldenRatio}
    eq3 = x + 2 + TribonacciConstant
    assert solve([eq1, eq3], x, y) == {x: -2 - TribonacciConstant, y: 1 + TribonacciConstant}

