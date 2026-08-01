
def test_X4():
    s1 = log(sin(x)/x).series()
    assert s1 == -x**2/6 - x**4/180 + O(x**6)
    assert log(series(sin(x)/x)).series() == s1

