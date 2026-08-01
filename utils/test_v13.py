
def test_V13():
    r1 = integrate(1/(6 + 3*cos(x) + 4*sin(x)), x)
    # expression not simplified, returns: -sqrt(11)*I*log(tan(x/2) + 4/3
    #   - sqrt(11)*I/3)/11 + sqrt(11)*I*log(tan(x/2) + 4/3 + sqrt(11)*I/3)/11
    assert r1.simplify() == 2*sqrt(11)*atan(sqrt(11)*(3*tan(x/2) + 4)/11)/11

