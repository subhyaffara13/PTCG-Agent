
def test_Limits_simple_2():
    assert limit(1000*x/(x**2 - 1), x, oo) == 0  # 182
    assert limit((x**2 - 5*x + 1)/(3*x + 7), x, oo) is oo  # 183
    assert limit((2*x**2 - x + 3)/(x**3 - 8*x + 5), x, oo) == 0  # 184
    assert limit((2*x**2 - 3*x - 4)/sqrt(x**4 + 1), x, oo) == 2  # 186
    assert limit((2*x + 3)/(x + root3(x)), x, oo) == 2  # 187
    assert limit(x**2/(10 + x*sqrt(x)), x, oo) is oo  # 188
    assert limit(root3(x**2 + 1)/(x + 1), x, oo) == 0  # 189
    assert limit(sqrt(x)/sqrt(x + sqrt(x + sqrt(x))), x, oo) == 1  # 190

