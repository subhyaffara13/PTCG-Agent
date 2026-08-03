import re

def test_re_im1652():
    x = Symbol('x')
    assert re(x) == re(conjugate(x))
    assert im(x) == - im(conjugate(x))
    assert im(x)*re(conjugate(x)) + im(conjugate(x)) * re(x) == 0

