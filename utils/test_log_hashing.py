
def test_log_hashing():
    assert x != log(log(x))
    assert hash(x) != hash(log(log(x)))
    assert log(x) != log(log(log(x)))

    e = 1/log(log(x) + log(log(x)))
    assert e.base.func is log
    e = 1/log(log(x) + log(log(log(x))))
    assert e.base.func is log

    e = log(log(x))
    assert e.func is log
    assert x.func is not log
    assert hash(log(log(x))) != hash(x)
    assert e != x

