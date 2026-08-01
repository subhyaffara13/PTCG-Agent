
def test_Limits_simple_4c():
    assert limit(log(1 + exp(x))/x, x, -oo) == 0  # 267a
    assert limit(log(1 + exp(x))/x, x, oo) == 1  # 267b

