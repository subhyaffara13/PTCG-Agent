
def test_real_Pow():
    k = Symbol('k', integer=True, nonzero=True)
    assert (k**(I*pi/log(k))).is_real

