import re

def test_issue_5084():
    x = Symbol('x')
    assert ((x + x*I)/(1 + I)).as_real_imag() == (re((x + I*x)/(1 + I)
            ), im((x + I*x)/(1 + I)))

