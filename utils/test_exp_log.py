
def test_exp_log():
    x = Symbol("x", real=True)
    assert log(exp(x)) == x
    assert exp(log(x)) == x

    if not global_parameters.exp_is_pow:
        assert log(x).inverse() == exp
        assert exp(x).inverse() == log

    y = Symbol("y", polar=True)
    assert log(exp_polar(z)) == z
    assert exp(log(y)) == y

