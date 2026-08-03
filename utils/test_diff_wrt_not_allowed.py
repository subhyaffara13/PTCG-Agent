import re

def test_diff_wrt_not_allowed():
    # issue 7027 included
    for wrt in (
            cos(x), re(x), x**2, x*y, 1 + x,
            Derivative(cos(x), x), Derivative(f(f(x)), x)):
        raises(ValueError, lambda: diff(f(x), wrt))
    # if we don't differentiate wrt then don't raise error
    assert diff(exp(x*y), x*y, 0) == exp(x*y)

