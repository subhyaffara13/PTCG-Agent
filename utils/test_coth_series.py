
def test_coth_series():
    x = Symbol('x')
    assert coth(x).series(x, 0, 8) == \
        1/x + x/3 - x**3/45 + 2*x**5/945 - x**7/4725 + O(x**8)

