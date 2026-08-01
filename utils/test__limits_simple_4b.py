
def test_Limits_simple_4b():
    #issue 3511
    assert limit(x - root3(x**3 - 1), x, oo) == 0  # 215

