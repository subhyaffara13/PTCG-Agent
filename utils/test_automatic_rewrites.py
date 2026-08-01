
def test_automatic_rewrites():
    assert maple_code(lucas(x)) == '(2^(-x)*((1 - sqrt(5))^x + (1 + sqrt(5))^x))'
    assert maple_code(sinc(x)) == '(piecewise(x <> 0, sin(x)/x, 1))'

