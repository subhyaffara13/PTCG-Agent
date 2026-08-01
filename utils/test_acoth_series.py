
def test_acoth_series():
    x = Symbol('x')
    assert acoth(x).series(x, 0, 10) == \
        -I*pi/2 + x + x**3/3 + x**5/5 + x**7/7 + x**9/9 + O(x**10)

