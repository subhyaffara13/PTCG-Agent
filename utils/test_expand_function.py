import re

def test_expand_function():
    assert expand(x + y) == x + y
    assert expand(x + y, complex=True) == I*im(x) + I*im(y) + re(x) + re(y)
    assert expand((x + y)**11, modulus=11) == x**11 + y**11

