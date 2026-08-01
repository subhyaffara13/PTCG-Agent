
def test_issue_21227():
    f = log(x)

    assert f.nseries(x, logx=y) == y
    assert f.nseries(x, logx=-x) == -x

    f = log(-log(x))

    assert f.nseries(x, logx=y) == log(-y)
    assert f.nseries(x, logx=-x) == log(x)

    f = log(log(x))

    assert f.nseries(x, logx=y) == log(y)
    assert f.nseries(x, logx=-x) == log(-x)
    assert f.nseries(x, logx=x) == log(x)

    f = log(log(log(1/x)))

    assert f.nseries(x, logx=y) == log(log(-y))
    assert f.nseries(x, logx=-y) == log(log(y))
    assert f.nseries(x, logx=x) == log(log(-x))
    assert f.nseries(x, logx=-x) == log(log(x))

