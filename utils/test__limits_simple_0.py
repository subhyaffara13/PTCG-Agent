
def test_Limits_simple_0():
    assert limit((2**(x + 1) + 3**(x + 1))/(2**x + 3**x), x, oo) == 3  # 175

