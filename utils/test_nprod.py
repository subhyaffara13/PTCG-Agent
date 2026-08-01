
def test_nprod():
    mp.dps = 15
    assert nprod(lambda k: exp(1/k**2), [1,inf], method='r').ae(exp(pi**2/6))
    assert nprod(lambda x: x**2, [1, 3]) == 36

