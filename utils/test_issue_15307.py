
def test_issue_15307():
    assert solve((y - 2, Mul(x + 3,x - 2, evaluate=False))) == \
        [{x: -3, y: 2}, {x: 2, y: 2}]
    assert solve((y - 2, Mul(3, x - 2, evaluate=False))) == \
        {x: 2, y: 2}
    assert solve((y - 2, Add(x + 4, x - 2, evaluate=False))) == \
        {x: -1, y: 2}
    eq1 = Eq(12513*x + 2*y - 219093, -5726*x - y)
    eq2 = Eq(-2*x + 8, 2*x - 40)
    assert solve([eq1, eq2]) == {x:12, y:75}

